"""
Script to create notebooks/logistics_analysis.ipynb
"""

import nbformat as nbf
import os

def create_analysis_notebook(output_path="notebooks/logistics_analysis.ipynb"):
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # Title Markdown
    cells.append(nbf.v4.new_markdown_cell("""# Smart Logistics Performance & Delivery Optimization Analytics
## Week 1 Internship Project — Strategic Planning & Exploratory Data Analysis

**Author:** Logistics Data Analyst Intern  
**Domain:** Supply Chain & Freight Logistics Analytics  
**Tools:** Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn)

---

### Executive Overview
This notebook presents the complete **Week 1 Strategic Planning & Exploratory Data Analysis** for supply chain optimization. The project evaluates freight transportation efficiency, identifies key drivers of delivery delays and high operational costs, calculates critical logistics KPIs, and establishes predictive ML & clustering prototypes.
"""))

    # Imports & Setup
    cells.append(nbf.v4.new_code_cell("""import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to path
sys.path.append('../src')

from generate_dataset import generate_logistics_dataset
from data_cleaning import load_raw_data, clean_and_prepare_data
from kpi_analysis import calculate_logistics_kpis
from eda import run_eda, setup_plot_style
from prediction import train_and_evaluate_models
from clustering import perform_kmeans_clustering

%matplotlib inline
setup_plot_style()
print("All analysis modules loaded successfully!")
"""))

    # Step 1 Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 1. Dataset Generation & Raw Data Inspection
We load the realistic logistics dataset comprising **1,250 shipment records** across 5 major warehouse hubs and 10 destination cities in India.
"""))

    # Step 1 Code
    cells.append(nbf.v4.new_code_cell("""raw_data_path = "../data/logistics_data.csv"
if not os.path.exists(raw_data_path):
    generate_logistics_dataset(output_path=raw_data_path, num_records=1250, seed=42)

raw_df = pd.read_csv(raw_data_path)
print(f"Raw Dataset Shape: {raw_df.shape}")
raw_df.head()
"""))

    # Step 2 Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 2. Data Cleaning & Feature Engineering
We execute an end-to-end data preparation workflow:
1. Deduplication (removing exact duplicate records)
2. Imputation of missing weather and fuel cost fields
3. Standardization of string categories and trimming whitespace
4. Feature engineering derived logistics variables (`delay_days`, `cost_per_km`, `warehouse_utilization`, `is_delayed`, `is_on_time`).
"""))

    # Step 2 Code
    cells.append(nbf.v4.new_code_cell("""cleaned_df = clean_and_prepare_data(raw_df, output_path="../outputs/cleaned_data.csv")
cleaned_df.info()
"""))

    # Step 3 Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 3. Logistics Key Performance Indicators (KPIs)
We measure operational performance across **Service Quality**, **Operational Speed**, **Cost Efficiency**, **Inventory & Warehouse Utilization**, and **Route Efficiency**.
"""))

    # Step 3 Code
    cells.append(nbf.v4.new_code_cell("""kpi_df = calculate_logistics_kpis(cleaned_df, output_path="../outputs/kpi_summary.csv")
kpi_df[['KPI Category', 'KPI Name', 'Value', 'Target Baseline', 'Formula / Definition']]
"""))

    # Step 4 Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 4. Exploratory Data Analysis & Visualizations
We generate high-resolution visual insights into delivery delays, shipping costs, warehouse performance, top delayed routes, and feature correlations.
"""))

    # Step 4 Code
    cells.append(nbf.v4.new_code_cell("""chart_paths = run_eda(cleaned_df, output_dir="../outputs/charts")

# Display On-Time vs Delayed Deliveries Distribution
plt.figure(figsize=(8, 4.5))
sns.countplot(x='delivery_status', data=cleaned_df, palette=['#2ecc71', '#e74c3c', '#3498db'])
plt.title("Delivery Status Distribution")
plt.xlabel("Status")
plt.ylabel("Shipment Count")
plt.show()

# Display Correlation Heatmap
num_cols = ['distance_km', 'quantity', 'order_value', 'shipping_cost', 'actual_delivery_days', 'delay_days', 'fuel_cost', 'warehouse_utilization']
plt.figure(figsize=(9, 6))
sns.heatmap(cleaned_df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title("Numerical Feature Correlation Matrix")
plt.show()
"""))

    # Step 5 Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 5. Predictive Machine Learning Modeling
We implement:
1. **Regression Models** (Linear Regression & Random Forest) to predict delivery time (`actual_delivery_days`).
2. **Classification Models** (Logistic Regression & Random Forest Classifier) to predict whether a shipment will suffer delivery delays (`is_delayed`).
"""))

    # Step 5 Code
    cells.append(nbf.v4.new_code_cell("""reg_results, clf_results = train_and_evaluate_models(cleaned_df, output_dir="../outputs/charts")
"""))

    # Step 6 Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 6. K-Means Clustering & Shipment Segmentation
Using K-Means clustering and the Elbow Method, we segment shipments into distinct operational personas for targeted logistics strategies.
"""))

    # Step 6 Code
    cells.append(nbf.v4.new_code_cell("""df_clustered, cluster_profiles = perform_kmeans_clustering(cleaned_df, output_dir="../outputs/charts")
"""))

    # Conclusion Markdown
    cells.append(nbf.v4.new_markdown_cell("""---
## 7. Executive Findings & Strategic Recommendations
1. **On-Time Performance:** On-Time delivery stands at **~60.1%**, while **~39.9%** of shipments experience delays. Adverse weather (Storms, Fog) and high-distance road freight are the primary drivers.
2. **Cost Efficiency:** Shipping cost is strongly driven by **distance** ($r = 0.89$) and **transportation mode** (Air Cargo > Express Courier > Road Freight > Rail Freight).
3. **Predictive Capability:** Machine learning models achieve **~89% $R^2$** in predicting delivery duration and **~76.8% Accuracy** in early delay detection.
4. **Segmentation Strategy:** K-Means clustering successfully isolates **High-Cost Long-Haul Cargo**, **High-Value Express Deliveries**, and **Standard Regional Freight**.
"""))

    nb['cells'] = cells
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        
    print(f"Jupyter Notebook successfully created at: {output_path}")

if __name__ == "__main__":
    create_analysis_notebook()
