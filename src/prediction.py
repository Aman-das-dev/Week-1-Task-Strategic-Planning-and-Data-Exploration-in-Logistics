"""
Predictive Modeling Module (Regression & Classification)
Project: Smart Logistics Performance & Delivery Optimization Analytics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, \
                            accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def train_and_evaluate_models(df, output_dir="outputs/charts"):
    """
    Train Regression models for delivery time & Classification models for delivery delay prediction.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Feature Preprocessing & One-Hot Encoding
    features = ['distance_km', 'quantity', 'order_value', 'fuel_cost', 
                'estimated_delivery_days', 'transportation_mode', 
                'weather_condition', 'warehouse', 'customer_segment']
                
    df_encoded = pd.get_dummies(df[features], columns=['transportation_mode', 'weather_condition', 'warehouse', 'customer_segment'], drop_first=True)
    
    # ----------------------------------------------------
    # A. REGRESSION: Predict Actual Delivery Time (Days)
    # ----------------------------------------------------
    y_reg = df['actual_delivery_days']
    X_reg = df_encoded.copy()
    
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )
    
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_reg, y_train_reg)
    y_pred_lr = lr.predict(X_test_reg)
    
    mae_lr = mean_absolute_error(y_test_reg, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test_reg, y_pred_lr))
    r2_lr = r2_score(y_test_reg, y_pred_lr)
    
    # Random Forest Regression
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_reg.fit(X_train_reg, y_train_reg)
    y_pred_rf_reg = rf_reg.predict(X_test_reg)
    
    mae_rf = mean_absolute_error(y_test_reg, y_pred_rf_reg)
    rmse_rf = np.sqrt(mean_squared_error(y_test_reg, y_pred_rf_reg))
    r2_rf = r2_score(y_test_reg, y_pred_rf_reg)
    
    regression_results = {
        "Linear Regression": {"MAE": round(mae_lr, 3), "RMSE": round(rmse_lr, 3), "R2": round(r2_lr, 3)},
        "Random Forest Regressor": {"MAE": round(mae_rf, 3), "RMSE": round(rmse_rf, 3), "R2": round(r2_rf, 3)}
    }
    
    # ----------------------------------------------------
    # B. CLASSIFICATION: Predict Delivery Delay (is_delayed)
    # ----------------------------------------------------
    y_clf = df['is_delayed']
    X_clf = df_encoded.copy()
    
    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
    )
    
    # Logistic Regression with Scaling
    scaler_clf = StandardScaler()
    X_train_scaled = scaler_clf.fit_transform(X_train_clf)
    X_test_scaled = scaler_clf.transform(X_test_clf)
    
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train_scaled, y_train_clf)
    y_pred_log = log_reg.predict(X_test_scaled)
    
    acc_log = accuracy_score(y_test_clf, y_pred_log)
    prec_log = precision_score(y_test_clf, y_pred_log, zero_division=0)
    rec_log = recall_score(y_test_clf, y_pred_log, zero_division=0)
    f1_log = f1_score(y_test_clf, y_pred_log, zero_division=0)
    
    # Random Forest Classifier
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(X_train_clf, y_train_clf)
    y_pred_rf_clf = rf_clf.predict(X_test_clf)
    
    acc_rf = accuracy_score(y_test_clf, y_pred_rf_clf)
    prec_rf = precision_score(y_test_clf, y_pred_rf_clf, zero_division=0)
    rec_rf = recall_score(y_test_clf, y_pred_rf_clf, zero_division=0)
    f1_rf = f1_score(y_test_clf, y_pred_rf_clf, zero_division=0)
    cm_rf = confusion_matrix(y_test_clf, y_pred_rf_clf)
    
    classification_results = {
        "Logistic Regression": {
            "Accuracy": round(acc_log, 3), "Precision": round(prec_log, 3), 
            "Recall": round(rec_log, 3), "F1-Score": round(f1_log, 3)
        },
        "Random Forest Classifier": {
            "Accuracy": round(acc_rf, 3), "Precision": round(prec_rf, 3), 
            "Recall": round(rec_rf, 3), "F1-Score": round(f1_rf, 3)
        }
    }
    
    # ----------------------------------------------------
    # Visualizations for Machine Learning Models
    # ----------------------------------------------------
    # 1. Feature Importance Plot
    plt.figure(figsize=(9, 6))
    importances = rf_clf.feature_importances_
    indices = np.argsort(importances)[::-1][:10]
    top_features = [X_clf.columns[i] for i in indices]
    top_importances = importances[indices]
    
    bars = plt.barh(top_features[::-1], top_importances[::-1], color='#8e44ad', edgecolor='black', alpha=0.85)
    plt.title("Top 10 Feature Importances for Delay Prediction (Random Forest)", pad=15)
    plt.xlabel("Relative Feature Importance Score")
    plt.ylabel("Feature")
    plt.tight_layout()
    feature_imp_path = os.path.join(output_dir, "feature_importance.png")
    plt.savefig(feature_imp_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Confusion Matrix Plot
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Predicted On-Time', 'Predicted Delayed'],
                yticklabels=['Actual On-Time', 'Actual Delayed'])
    plt.title("Confusion Matrix: Random Forest Delay Classifier", pad=15)
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    plt.close()

    print("\n--- Predictive Analytics Model Performance Summary ---")
    print("\n1. Regression Models (Target: Actual Delivery Days):")
    for model_name, metrics in regression_results.items():
        print(f" - {model_name}: MAE={metrics['MAE']}, RMSE={metrics['RMSE']}, R²={metrics['R2']}")
        
    print("\n2. Classification Models (Target: Delivery Delay Status):")
    for model_name, metrics in classification_results.items():
        print(f" - {model_name}: Accuracy={metrics['Accuracy']}, Precision={metrics['Precision']}, Recall={metrics['Recall']}, F1={metrics['F1-Score']}")
        
    return regression_results, classification_results

if __name__ == "__main__":
    from data_cleaning import load_raw_data, clean_and_prepare_data
    df = clean_and_prepare_data(load_raw_data())
    train_and_evaluate_models(df)
