"""
Data Cleaning & Feature Engineering Module
Project: Smart Logistics Performance & Delivery Optimization Analytics
"""

import pandas as pd
import numpy as np
import os

def load_raw_data(file_path="data/logistics_data.csv"):
    """Load raw dataset from CSV file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found at: {file_path}")
    df = pd.read_csv(file_path)
    return df

def clean_and_prepare_data(df, output_path="outputs/cleaned_data.csv"):
    """
    Perform full data cleaning and feature engineering workflow:
    1. Duplicate Removal
    2. Missing Value Imputation
    3. Category & String Standardization
    4. Datetime Conversion
    5. Feature Engineering of Logistics KPIs & Ratios
    """
    df_clean = df.copy()
    
    # 1. Remove duplicate records
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    duplicates_removed = initial_rows - len(df_clean)
    
    # 2. String Standardization & Whitespace Trimming
    string_cols = ['shipment_id', 'warehouse', 'origin_city', 'destination_city', 
                   'product_category', 'transportation_mode', 'delivery_status', 
                   'customer_segment', 'weather_condition']
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
    # 3. Handle Missing Values
    # Replace 'nan' string resulting from str conversion back to np.nan if any
    df_clean['weather_condition'] = df_clean['weather_condition'].replace(['nan', 'None'], np.nan)
    if df_clean['weather_condition'].isnull().sum() > 0:
        mode_weather = df_clean['weather_condition'].mode()[0]
        df_clean['weather_condition'] = df_clean['weather_condition'].fillna(mode_weather)
        
    if df_clean['fuel_cost'].isnull().sum() > 0:
        median_fuel = df_clean['fuel_cost'].median()
        df_clean['fuel_cost'] = df_clean['fuel_cost'].fillna(median_fuel)
        
    # 4. Correct Data Types & Dates
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])
    
    numeric_cols = ['quantity', 'order_value', 'distance_km', 'shipping_cost', 
                    'estimated_delivery_days', 'actual_delivery_days', 'delay_days', 
                    'inventory_level', 'warehouse_capacity', 'fuel_cost']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
    # 5. Feature Engineering
    # Recalculate delay_days precisely
    df_clean['delay_days'] = (df_clean['actual_delivery_days'] - df_clean['estimated_delivery_days']).clip(lower=0)
    df_clean['delivery_time'] = df_clean['actual_delivery_days']
    df_clean['cost_per_km'] = np.round(df_clean['shipping_cost'] / df_clean['distance_km'], 4)
    df_clean['cost_per_shipment'] = df_clean['shipping_cost']
    df_clean['is_delayed'] = (df_clean['delay_days'] > 0).astype(int)
    df_clean['is_on_time'] = (df_clean['delay_days'] == 0).astype(int)
    df_clean['warehouse_utilization'] = np.round((df_clean['inventory_level'] / df_clean['warehouse_capacity']) * 100, 2)
    df_clean['route'] = df_clean['origin_city'] + " -> " + df_clean['destination_city']
    
    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    
    print(f"Data Cleaning Complete:")
    print(f" - Rows before: {initial_rows}, Rows after: {len(df_clean)} ({duplicates_removed} duplicates removed)")
    print(f" - Missing values handled for weather_condition and fuel_cost")
    print(f" - Derived features created: delay_days, delivery_time, cost_per_km, cost_per_shipment, is_delayed, is_on_time, warehouse_utilization, route")
    print(f" - Saved cleaned dataset to: {output_path}")
    
    return df_clean

if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df = clean_and_prepare_data(raw_df)
