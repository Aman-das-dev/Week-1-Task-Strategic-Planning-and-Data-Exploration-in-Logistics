"""
Advanced Data Preprocessing & Pipeline Module (Week 2 Task)
Project: Smart Logistics Performance & Delivery Optimization Analytics
Implements:
1. Missing Value Imputation
2. Outlier Detection (IQR Method) & Winsorization Capping
3. Categorical Feature Encoding (One-Hot Encoding)
4. Numerical Feature Normalization & Standardization (MinMax vs. Standard Scaling)
5. Validation and Pipeline Visualization Charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def setup_plot_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10

def load_and_validate_data(file_path="data/logistics_data.csv"):
    """Load dataset and perform initial health check and deduplication."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"\n[Ingestion] Data loaded successfully. Initial Shape: {df.shape}")
    
    # Check duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()
        print(f"[Ingestion] Identified and removed {dup_count} duplicate records. Cleaned Shape: {df.shape}")
    else:
        print("[Ingestion] No duplicate records found.")
        
    print(f"[Ingestion] Missing values count per column:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    return df

def impute_missing_values(df):
    """
    Impute missing values using logical business rules:
    - weather_condition (categorical) -> Mode imputation (most common weather)
    - fuel_cost (numerical) -> Median imputation (less sensitive to outliers)
    """
    df_imputed = df.copy()
    
    # 1. Weather Imputation
    if 'weather_condition' in df_imputed.columns and df_imputed['weather_condition'].isnull().sum() > 0:
        weather_mode = df_imputed['weather_condition'].mode()[0]
        df_imputed['weather_condition'] = df_imputed['weather_condition'].fillna(weather_mode)
        print(f"[Imputation] Imputed missing weather_condition with mode: '{weather_mode}'")
        
    # 2. Fuel Cost Imputation
    if 'fuel_cost' in df_imputed.columns and df_imputed['fuel_cost'].isnull().sum() > 0:
        fuel_median = df_imputed['fuel_cost'].median()
        df_imputed['fuel_cost'] = df_imputed['fuel_cost'].fillna(fuel_median)
        print(f"[Imputation] Imputed missing fuel_cost with median: ${fuel_median:.2f}")
        
    return df_imputed

def detect_and_cap_outliers(df, cols_to_check=['shipping_cost', 'quantity', 'order_value', 'distance_km']):
    """
    Detect outliers using the Interquartile Range (IQR) method and cap them (Winsorization)
    at 1.5 * IQR limits to avoid data loss while securing model stability.
    """
    df_capped = df.copy()
    
    fig, axes = plt.subplots(len(cols_to_check), 2, figsize=(10, len(cols_to_check) * 2.5))
    setup_plot_style()
    
    for idx, col in enumerate(cols_to_check):
        # Calculate IQR
        Q1 = df_capped[col].quantile(0.25)
        Q3 = df_capped[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Count outliers before capping
        outliers_count = ((df_capped[col] < lower_bound) | (df_capped[col] > upper_bound)).sum()
        
        # Plot Before Capping
        sns.boxplot(x=df_capped[col], ax=axes[idx, 0], color='#e74c3c')
        axes[idx, 0].set_title(f"{col} - Before Capping ({outliers_count} Outliers)")
        
        # Perform Capping (Winsorization)
        df_capped[col] = np.clip(df_capped[col], lower_bound, upper_bound)
        
        # Plot After Capping
        sns.boxplot(x=df_capped[col], ax=axes[idx, 1], color='#2ecc71')
        axes[idx, 1].set_title(f"{col} - After Capping")
        
        print(f"[Outliers] Identified & capped {outliers_count} outliers in '{col}' [Bounds: {lower_bound:.2f} to {upper_bound:.2f}]")
        
    plt.tight_layout()
    chart_path = "outputs/charts/outliers_comparison.png"
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Outliers] Outliers boxplot saved to: {chart_path}")
    
    return df_capped

def compare_scaling_methods(df, cols_to_scale=['shipping_cost', 'distance_km']):
    """
    Compare MinMaxScaler (Normalization) vs StandardScaler (Standardization).
    Saves a visualization showing distribution profiles.
    """
    df_scaling = df.copy()
    
    scaler_std = StandardScaler()
    scaler_minmax = MinMaxScaler()
    
    # Scale test feature
    col = cols_to_scale[0] # shipping_cost
    original_data = df_scaling[col].values.reshape(-1, 1)
    
    std_scaled = scaler_std.fit_transform(original_data).flatten()
    minmax_scaled = scaler_minmax.fit_transform(original_data).flatten()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    setup_plot_style()
    
    # Original
    sns.histplot(df_scaling[col], kde=True, ax=axes[0], color='#34495e', edgecolor='black')
    axes[0].set_title(f"Original {col}\n(Mean: {df_scaling[col].mean():.2f}, Std: {df_scaling[col].std():.2f})")
    
    # Standard Scaled (Z-Score)
    sns.histplot(std_scaled, kde=True, ax=axes[1], color='#9b59b6', edgecolor='black')
    axes[1].set_title(f"Standardized (Z-Score Scaling)\n(Mean: {std_scaled.mean():.1f}, Std: {std_scaled.std():.1f})")
    
    # MinMax Scaled (Normalized)
    sns.histplot(minmax_scaled, kde=True, ax=axes[2], color='#3498db', edgecolor='black')
    axes[2].set_title(f"Normalized (MinMax [0,1] Scaling)\n(Min: {minmax_scaled.min():.1f}, Max: {minmax_scaled.max():.1f})")
    
    plt.tight_layout()
    chart_path = "outputs/charts/scaling_comparison.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Scaling] Scaling comparison histogram saved to: {chart_path}")
    
    # Apply Standard Scaling to numeric columns for output
    for c in cols_to_scale:
        df_scaling[f"{c}_standardized"] = scaler_std.fit_transform(df_scaling[[c]])
        df_scaling[f"{c}_normalized"] = scaler_minmax.fit_transform(df_scaling[[c]])
        
    return df_scaling

def run_preprocessing_pipeline():
    print("=" * 80)
    print("      LOGISTICS DATA PREPROCESSING & DATA QUALITY PIPELINE (WEEK 2)     ")
    print("=" * 80)
    
    # 1. Ingestion
    df = load_and_validate_data("data/logistics_data.csv")
    
    # 2. Imputation
    df_imputed = impute_missing_values(df)
    
    # 3. Outlier Handling
    df_capped = detect_and_cap_outliers(df_imputed)
    
    # 4. Standardizing Text / Whitespaces
    df_capped['destination_city'] = df_capped['destination_city'].str.strip()
    df_capped['product_category'] = df_capped['product_category'].str.strip()
    
    # 5. Scaling Comparison & Implementation
    df_scaled = compare_scaling_methods(df_capped)
    
    # 6. One-Hot Encoding
    categorical_cols = ['transportation_mode', 'weather_condition', 'warehouse', 'customer_segment']
    df_preprocessed = pd.get_dummies(df_scaled, columns=categorical_cols, drop_first=True)
    
    # Save Preprocessed Dataset
    output_csv = "outputs/preprocessed_data.csv"
    df_preprocessed.to_csv(output_csv, index=False)
    print(f"\n[Pipeline] Completed successfully! Saved preprocessed data to: {output_csv}")
    print(f"[Pipeline] Final Preprocessed Shape: {df_preprocessed.shape}")
    print("=" * 80)

if __name__ == "__main__":
    run_preprocessing_pipeline()
