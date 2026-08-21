"""
Main Pipeline Script
Project: Smart Logistics Performance & Delivery Optimization Analytics
Week 1 Logistics Data Analyst Internship Submission
"""

import os
import sys

# Ensure src directory is in Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from generate_dataset import generate_logistics_dataset
from data_cleaning import load_raw_data, clean_and_prepare_data
from kpi_analysis import calculate_logistics_kpis
from eda import run_eda
from prediction import train_and_evaluate_models
from clustering import perform_kmeans_clustering

def run_pipeline():
    print("=" * 80)
    print("      SMART LOGISTICS PERFORMANCE & DELIVERY OPTIMIZATION ANALYTICS      ")
    print("         Week 1 Project Pipeline — Logistics Data Analyst Intern          ")
    print("=" * 80)
    
    # Step 1: Data Generation / Verification
    raw_data_path = "data/logistics_data.csv"
    if not os.path.exists(raw_data_path):
        print("\n[Step 1/6] Generating realistic synthetic logistics dataset...")
        generate_logistics_dataset(output_path=raw_data_path, num_records=1250, seed=42)
    else:
        print(f"\n[Step 1/6] Found existing raw dataset at: {raw_data_path}")
        
    # Step 2: Data Cleaning & Feature Engineering
    print("\n[Step 2/6] Running Data Cleaning & Feature Engineering...")
    raw_df = load_raw_data(raw_data_path)
    cleaned_df = clean_and_prepare_data(raw_df, output_path="outputs/cleaned_data.csv")
    
    # Step 3: Key Performance Indicator (KPI) Calculation
    print("\n[Step 3/6] Calculating Key Performance Indicators (KPIs)...")
    kpi_df = calculate_logistics_kpis(cleaned_df, output_path="outputs/kpi_summary.csv")
    
    # Step 4: Exploratory Data Analysis & Visualization
    print("\n[Step 4/6] Executing Exploratory Data Analysis (EDA) & Chart Generation...")
    chart_paths = run_eda(cleaned_df, output_dir="outputs/charts")
    
    # Step 5: Predictive Analytics (Regression & Classification)
    print("\n[Step 5/6] Building & Evaluating Predictive Machine Learning Models...")
    reg_results, clf_results = train_and_evaluate_models(cleaned_df, output_dir="outputs/charts")
    
    # Step 6: Clustering & Segmentation Analysis
    print("\n[Step 6/6] Executing K-Means Clustering & Segmentation Analysis...")
    df_clustered, cluster_profiles = perform_kmeans_clustering(cleaned_df, output_dir="outputs/charts")
    
    print("\n" + "=" * 80)
    print("                   PROJECT EXECUTION COMPLETED SUCCESSFULLY!                  ")
    print("=" * 80)
    print("Summary of Generated Deliverables:")
    print(" - Raw Dataset: data/logistics_data.csv (1,250 records)")
    print(" - Cleaned Dataset: outputs/cleaned_data.csv")
    print(" - KPI Summary: outputs/kpi_summary.csv")
    print(f" - Charts Generated: {len(chart_paths)} charts saved in outputs/charts/")
    print(" - Primary Submission Document: docs/Strategic_Planning_Report.docx")
    print("=" * 80)

if __name__ == "__main__":
    run_pipeline()
