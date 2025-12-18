# src/pipelines/model_training.py

import pandas as pd
import joblib
import os
import sys
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

try:
    from src.utils.config_loader import load_config
except ImportError:
    import yaml
    def load_config(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

def get_feature_importance(pipeline, top_n=20):
    """
    Extracts and prints the top positive and
    negative coefficients from the model.
    """
    print(f"\n--- Feature Importance Analysis (Top {top_n}) ---")

    # extract model & preprocessor
    model = pipeline.named_steps["classifier"]
    preprocessor = pipeline.named_steps["preprocessor"]

    # get feature names from preprocessor
    try:
        feature_names = preprocessor.get_feature_names_out()
    except AttributeError:
        print("Warning: Unable to extract feature names from preprocessor.")
        return

    # Logistic Regression
    if hasattr(model, "coeff_"):
        # get coefficients & flatten to 1D array
        coefs = model.coef_[0]

        # create dataframe for easy sorting
        importance = pd.DataFrame({"Feature": feature_names, "Coefficient": coefs})

        # separate good and bad predictors
        success_features = importance[importance["Coefficient"] > 0].copy()
        failure_features = importance[importance["Coefficient"] < 0].copy()

        # print top predictors for sucess
        print("\nTop Predictors for SUCCESS:")
        if not success_features.empty:
            print(
                success_features.sort_values(by="Coefficient", ascending=False)
                .head(top_n)
                .to_string(index=False)
            )
        else:
            print("   (No positive features found)")

        # print top predictors for failure
        print("\nTop Predictors for FAILURE:")
        if not failure_features.empty:
            print(
                failure_features.sort_values(by="Coefficient", ascending=True)
                .head(top_n)
                .to_string(index=False)
            )
        else:
            print("   (No negative features found)")

    # Random Forest
    elif hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        importance = pd.DataFrame({"Feature": feature_names, "Importance": importances})

        print("\nTop Most Important Features (Direction Unknown):")
        print(importance.sort_values(by="Importance", ascending=False).head(top_n).to_string(index=False))
        
    else:
        print("Model type does not support direct feature importance extraction.")

def run_training_pipeline(input_path: str, model_path: str):
    """
    Trains a Logistic Regression model and saves it
    """
    config = load_config("params.yaml")
    model_config = config.get("model", {})
     # default to logistic if current config not valid
    model_type = model_config.get("type", "logistic")

    if mlflow.active_run():
        print("⚠️ Found an active run. Ending it now...")
        mlflow.end_run()

    print("Starting Model Training (with MLflow)...")
    print(f"Selected model: {model_type.upper()}")
    print(f"Loading data from {input_path}...")

    mlflow.set_experiment("clinical_trials_outcome")

    if not os.path.exists(input_path):
        print(f"CRITICAL: Input data file {input_path} does not exists.")
        sys.exit(1)

    df = pd.read_csv(input_path)
    print("Data loaded successfully.")

    target_col = "target_outcome"
    if target_col not in df.columns:
        print(f"CRITICAL: Target column '{target_col}' not found in data.")
        sys.exit(1)

    X = df.drop(columns=[target_col])
    y = df[target_col]

    print(f"Features detected: {X.shape[1]}")
    print(f"Target distribution:\n{y.value_counts(normalize=True)}")

    # silence MLflow warning
    # logistic regression uses floats anyway
    X = X.astype(float)

    seed = config.get("train", {}).get("random_state", 42)
    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    with mlflow.start_run():
        # only need to scale 'enrollment_log'...everything else is already 0-1
        numeric_features = ["enrollment_log"]
        # ensure column exists
        numeric_features = [col for col in numeric_features if col in X.columns]

        preprocessor = ColumnTransformer(
            transformers=[("num", StandardScaler(), numeric_features)],
            remainder="passthrough",  # don't touch other columns
        )

        # model selection
        if model_type == "random_forest":
            rf_params = model_config.get("random_forsts", {})
            clf = RandomForestClassifier(
                n_estimators=rf_params.get("n_estimators", 100),
                max_depth=rf_params.get("max_depth", 10),
                class_weight="balanced",
                n_jobs=1,
                random_state=seed
            )
            # log specific random forest params
            mlflow.log_params(rf_params)
            mlflow.log_param("model_type", "RandomForest")

        else:
            # default to Logistic Regression
            lr_params = model_config.get("logistic", {})
            clf = LogisticRegression(
                C=lr_params.get("C", 1.0),
                solver=lr_params.get("solver", "liblinear"),
                max_iter=lr_params.get("max_iter", 1000),
                class_weight="balanced",
                random_state=seed
            )
            # log specific LR params
            mlflow.log_params(lr_params)
            mlflow.log_param("model_type", "LogisticRegression")

        # build model pipeline
        model_pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", clf),
            ]
        )

        print("Training the model...")
        model_pipeline.fit(X_train, y_train)
        print("Model training complete.\n")

        print("--- Evaluation on Test Set ---")
        y_pred = model_pipeline.predict(X_test)

        # get % confidence
        y_proba = model_pipeline.predict_proba(X_test)[:, 1]

        # terminal report
        print(classification_report(y_test, y_pred))
        # analyze feature importance
        get_feature_importance(model_pipeline, top_n=10)

        roc = roc_auc_score(y_test, y_proba)
        report = classification_report(y_test, y_pred, output_dict=True)

        metrics = {
            "roc_auc": roc,
            "precision_class_1": report["1"]["precision"],
            "recall_class_1": report["1"]["recall"],
            "f1_class_1": report["1"]["f1-score"],
        }
        mlflow.log_metrics(metrics)
        print(f"Logged Metrics: ROC-AUC={roc:.4f}\n")

        input_example = X_train.iloc[:5]
        signature = infer_signature(
            input_example, model_pipeline.predict(input_example)
        )

        # log model
        mlflow.sklearn.log_model(
            sk_model=model_pipeline,
            name="model",
            input_example=input_example,
            signature=signature,
        )

        try:
            model = model_pipeline.named_steps["classifier"]
            feature_names = model_pipeline.named_steps[
                "preprocessor"
            ].get_feature_names_out()

            imp_df = None

            # Case A: Logistic Regression (has 'coef_')
            if hasattr(model, "coef_"):
                imp_df = pd.DataFrame({
                    "Feature": feature_names, 
                    "Value": model.coef_[0]  # Rename to 'Value' to be generic
                }).sort_values(by="Value", ascending=False)
                
            # Case B: Random Forest (has 'feature_importances_')
            elif hasattr(model, "feature_importances_"):
                imp_df = pd.DataFrame({
                    "Feature": feature_names, 
                    "Value": model.feature_importances_
                }).sort_values(by="Value", ascending=False)

            # Save if data was found
            if imp_df is not None:
                imp_df.to_csv("feature_importance.csv", index=False)
                mlflow.log_artifact("feature_importance.csv")
                os.remove("feature_importance.csv") # Clean up
                print("✅ Feature importance CSV logged to MLflow.")
            else:
                print("⚠️ Model does not support feature importance extraction.")
                
        except Exception as e:
            print(f"⚠️ Skipping feature importance logging: {e}")

    # save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model_pipeline, model_path)
    print(f"Model saved to: {model_path}")
