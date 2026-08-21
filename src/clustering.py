"""
Clustering & Segmentation Module (K-Means)
Project: Smart Logistics Performance & Delivery Optimization Analytics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def perform_kmeans_clustering(df, output_dir="outputs/charts"):
    """
    Perform K-Means clustering to segment shipments/routes based on key operational features.
    Saves Elbow curve plot and Cluster Scatter Plot.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Feature Selection & Standard Scaling
    cluster_features = ['distance_km', 'shipping_cost', 'quantity', 'order_value', 'actual_delivery_days']
    X_cluster = df[cluster_features].copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)
    
    # 2. Elbow Method for Optimal K
    inertias = []
    k_range = range(1, 11)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        
    plt.figure(figsize=(8, 5))
    plt.plot(k_range, inertias, marker='o', linestyle='--', color='#2980b9', linewidth=2, markersize=8)
    plt.title("K-Means Elbow Method for Optimal Cluster Determination", pad=15)
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Sum of Squared Distances (Inertia)")
    plt.xticks(k_range)
    plt.grid(True)
    plt.tight_layout()
    elbow_path = os.path.join(output_dir, "kmeans_elbow_curve.png")
    plt.savefig(elbow_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Fit K-Means with Optimal K = 3
    optimal_k = 3
    kmeans_opt = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans_opt.fit_predict(X_scaled)
    
    df_clustered = df.copy()
    df_clustered['cluster'] = cluster_labels
    
    # Map descriptive personas based on cluster stats
    cluster_profiles = df_clustered.groupby('cluster')[cluster_features].mean().round(2)
    
    cluster_names = {}
    for cl in range(optimal_k):
        dist = cluster_profiles.loc[cl, 'distance_km']
        cost = cluster_profiles.loc[cl, 'shipping_cost']
        val = cluster_profiles.loc[cl, 'order_value']
        
        if cost > df['shipping_cost'].mean() and dist > df['distance_km'].mean():
            cluster_names[cl] = "High-Cost Long-Haul Cargo"
        elif val > df['order_value'].mean():
            cluster_names[cl] = "High-Value Express Deliveries"
        else:
            cluster_names[cl] = "Standard Regional Freight"
            
    df_clustered['cluster_name'] = df_clustered['cluster'].map(cluster_names)
    cluster_profiles['Persona'] = [cluster_names[i] for i in cluster_profiles.index]
    
    # 4. Scatter Plot Visualization of Clusters (Distance vs Cost)
    plt.figure(figsize=(9, 6))
    palette = sns.color_palette("Set1", optimal_k)
    sns.scatterplot(
        x='distance_km', y='shipping_cost', hue='cluster_name',
        data=df_clustered, palette=palette, s=70, alpha=0.8, edgecolor='k'
    )
    plt.title("Logistics Shipment Segmentation Clusters (Distance vs Cost)", pad=15)
    plt.xlabel("Distance (km)")
    plt.ylabel("Shipping Cost ($)")
    plt.legend(title="Shipment Cluster Persona", loc="upper left")
    plt.tight_layout()
    scatter_path = os.path.join(output_dir, "customer_clusters.png")
    plt.savefig(scatter_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n--- K-Means Logistics Segmentation Profiles ---")
    print(cluster_profiles[['Persona'] + cluster_features])
    
    return df_clustered, cluster_profiles

if __name__ == "__main__":
    from data_cleaning import load_raw_data, clean_and_prepare_data
    df = clean_and_prepare_data(load_raw_data())
    perform_kmeans_clustering(df)
