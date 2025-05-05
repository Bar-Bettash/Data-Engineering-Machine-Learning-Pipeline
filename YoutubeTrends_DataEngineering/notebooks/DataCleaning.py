import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import os

# Detect categorical and numerical columns
def detect_column_types(df):
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    return categorical_cols, numeric_cols

# Train imputation model
def train_imputation_model(df, target_column, model_dir='impute_models', random_state=42):
    print(f"\nTraining model to impute: {target_column}")
    os.makedirs(model_dir, exist_ok=True)

    # Remove fully-null rows
    df = df.dropna(axis=0, how='all')

    # Detect column types
    categorical_cols, numeric_cols = detect_column_types(df)

    # Only use fully available columns as features (excluding the target)
    features = [col for col in df.columns if col != target_column and df[col].isnull().sum() == 0]

    # Prepare train data
    mask = df[target_column].notna()
    X = df.loc[mask, features]
    y = df.loc[mask, target_column]

    if X.shape[0] < 10:
        print(f"Not enough data to train model for {target_column}. Skipping.")
        return None, None

    # Determine task type
    if pd.api.types.is_numeric_dtype(y):
        model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        scorer = mean_squared_error
        model_type = "regression"
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        scorer = accuracy_score
        model_type = "classification"

    # Separate usable features
    cat_features = [col for col in features if col in categorical_cols]
    num_features = [col for col in features if col in numeric_cols]

    # Preprocessing pipeline
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
    ])

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    # Train and evaluate
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    score = scorer(y_test, y_pred)
    print(f"Validation {'MSE' if model_type == 'regression' else 'Accuracy'}: {score:.4f}")

    # Save model
    model_path = os.path.join(model_dir, f'{target_column}_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")
    return pipeline, features

# Apply trained model to impute
def impute_missing_values(df, target_column, model_dir='impute_models'):
    print(f"\nImputing values for: {target_column}")
    model_path = os.path.join(model_dir, f'{target_column}_model.pkl')
    if not os.path.exists(model_path):
        print(f"No trained model found for {target_column}. Skipping.")
        return df

    pipeline = joblib.load(model_path)
    preprocessor = pipeline.named_steps['preprocessor']
    feature_names = preprocessor.feature_names_in_

    mask = df[target_column].isnull()
    if mask.sum() == 0:
        print("No missing values to impute.")
        return df

    X_missing = df.loc[mask, feature_names].copy()
    predicted_values = pipeline.predict(X_missing)

    if pd.api.types.is_numeric_dtype(df[target_column]):
        predicted_values = np.maximum(0, predicted_values)

    df.loc[mask, target_column] = predicted_values
    print(f"Imputed {mask.sum()} missing values for {target_column}")
    return df

# Main pipeline to impute all valid float/int/object columns
def fill_null_ML(df, model_dir='impute_models'):
    print("🚀 Starting ML-based imputation (only for float, int, object)...")
    df = df.copy()
    
    # Only process float/int/object columns
    target_cols = df.columns[
        df.isnull().sum() > 0
    ]
    eligible_cols = [
        col for col in target_cols
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_object_dtype(df[col])
    ]

    for col in eligible_cols:
        model, _ = train_imputation_model(df, col, model_dir=model_dir)
        if model is not None:
            df = impute_missing_values(df, col, model_dir=model_dir)
    
    print("✅ Imputation completed.")
    return df
