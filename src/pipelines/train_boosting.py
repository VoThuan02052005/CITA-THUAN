import os
import re
import joblib
import pandas as pd
import time
from src.features.build_feature import build_features
from src.model.boosting import build_boosting_models
from src.utils.metrics import evaluate_regression
from src.utils.logger import Logger

logger = Logger("train_boosting")


def _sanitize_columns(df):
    """Thay thế ký tự đặc biệt trong tên cột (LightGBM không hỗ trợ JSON chars)."""
    df.columns = [re.sub(r'[^\w]', '_', c) for c in df.columns]
    return df


def train_boosting(data_path):
    logger.info("Starting boosting models training pipeline")
    
    # Load data
    logger.info(f"Loading data from {data_path}")
    data = pd.read_csv(data_path)
    
    # Feature engineering
    logger.info("Building features")
    features = build_features(data)
    X_train, X_test = features["X_train"], features["X_test"]
    y_train, y_test = features["y_train"], features["y_test"]

    # Sanitize feature names (LightGBM/CatBoost yêu cầu tên cột không có ký tự đặc biệt)
    X_train = _sanitize_columns(X_train)
    X_test = _sanitize_columns(X_test)
    
    models = build_boosting_models()
    results = {}
    
    # Training and Evaluation
    for name, model in models.items():
        logger.info(f"Training {name} model")
        start_time = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start_time
        
        logger.info(f"Evaluating {name}")
        y_pred = model.predict(X_test)
        metrics = evaluate_regression(y_test, y_pred)
        metrics["train_time"] = train_time
        results[name] = metrics
        
        logger.info(f"{name} Results: {metrics}")
        
        # Save each model
        os.makedirs("models", exist_ok=True)
        model_path = f"models/boosting_{name.lower()}_model.joblib"
        joblib.dump(model, model_path)
        logger.success(f"{name} model saved to {model_path}")
    
    return results

if __name__ == "__main__":
    DATA_PATH = "data/staging/data_sau_clean.csv"
    train_boosting(DATA_PATH)
