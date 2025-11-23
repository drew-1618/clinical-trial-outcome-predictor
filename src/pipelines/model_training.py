# src/pipelines/model_training.py

import pandas as pd
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def get_feature_importance(pipeline, top_n=20):
    """
    Extracts and prints the top positive and negative coefficients from the model.
    """
    print(f"\n--- Feature Importance Analysis (Top {top_n}) ---")

    # extract model & preprocessor
    model = pipeline.named_steps['classifier']
    preprocessor = pipeline.named_steps['preprocessor']

    # get feature names from preprocessor
    try:
        feature_names = preprocessor.get_feature_names_out()
    except AttributeError:
        print("Warning: Unable to extract feature names from preprocessor.")
        return

    # get coefficients & flatten to 1D array
    coefs = model.coef_[0]

    # create dataframe for easy sorting
    importance = pd.DataFrame({
        'Feature' : feature_names,
        'Coefficient' : coefs
    })

    # separate good and bad predictors
    success_features = importance[importance['Coefficient'] > 0].copy()
    failure_features = importance[importance['Coefficient'] < 0].copy()

    # print top predictors for sucess
    print("\nTop Predictors for SUCCESS:")
    if not success_features.empty:
        print(success_features.sort_values(by='Coefficient', ascending=False).head(top_n).to_string(index=False))
    else:
        print("   (No positive features found)")

    # print top predictors for failure
    print("\nTop Predictors for FAILURE:")
    if not failure_features.empty:
        print(failure_features.sort_values(by='Coefficient', ascending=True).head(top_n).to_string(index=False))
    else:
        print("   (No negative features found)")


def run_training_pipeline(input_path: str, model_path: str):
    """
    Trains a Logistic Regression model and saves it
    """
    print("Starting Model Training...")
    print(f"Loading data from {input_path}...")

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

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # only need to scale 'enrollment_log'...everything else is already 0-1
    numeric_features = ['enrollment_log']
    # ensure column exists
    numeric_features = [col for col in numeric_features if col in X.columns]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features)
        ],
        remainder='passthrough'  # don't touch other columns
    )

    # build model pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])

    print("Training the model...")
    model_pipeline.fit(X_train, y_train)
    print("Model training complete.\n")

    print("--- Evaluation on Test Set ---")
    y_pred = model_pipeline.predict(X_test)

    # get % confidence
    y_proba = model_pipeline.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}\n")

    # analyze feature importance
    get_feature_importance(model_pipeline, top_n=10)

    # save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model_pipeline, model_path)
    print(f"Model saved to: {model_path}")
