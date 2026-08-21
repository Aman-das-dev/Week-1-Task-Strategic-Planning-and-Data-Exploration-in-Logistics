"""
Exploratory Data Analysis (EDA) Module
Project: Smart Logistics Performance & Delivery Optimization Analytics
Generates high-resolution visualizations for delivery, cost, warehouse, route, product, and correlation analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def setup_plot_style():
    """Set global Matplotlib and Seaborn aesthetic configurations."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['figure.titlesize'] = 16

def run_eda(df, output_dir="outputs/charts"):
    """
    Generate and save all 14 EDA visualizations into output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    setup_plot_style()
    
    saved_charts = []
    
    # 1. Delivery Analysis: On-Time vs Delayed Deliveries
    plt.figure(figsize=(8, 5))
    status_counts = df['delivery_status'].value_counts()
    colors = {'On-Time': '#2ecc71', 'Delayed': '#e74c3c', 'Early': '#3498db'}
    bar_colors = [colors.get(s, '#95a5a6') for s in status_counts.index]
    
    bars = plt.bar(status_counts.index, status_counts.values, color=bar_colors, width=0.5, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        pct = (height / len(df)) * 100
        plt.text(bar.get_x() + bar.get_width()/2., height + 10, f'{height}\n({pct:.1f}%)',
                 ha='center', va='bottom', fontweight='bold', fontsize=10)
                 
    plt.title("Delivery Status Distribution (On-Time vs Delayed vs Early)", pad=15)
    plt.xlabel("Delivery Status")
    plt.ylabel("Number of Shipments")
    plt.ylim(0, max(status_counts.values) * 1.18)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "delivery_status_distribution.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)
    
    # 2. Delivery Delay Distribution (Histogram / KDE)
    plt.figure(figsize=(9, 5))
    sns.histplot(df['delay_days'], bins=15, kde=True, color='#e74c3c', edgecolor='black', alpha=0.6)
    plt.title("Distribution of Delivery Delay Days", pad=15)
    plt.xlabel("Delay Duration (Days)")
    plt.ylabel("Frequency (Shipment Count)")
    plt.axvline(df['delay_days'].mean(), color='black', linestyle='--', linewidth=2, label=f"Mean Delay: {df['delay_days'].mean():.2f} days")
    plt.legend()
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "delay_days_distribution.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)
    
    # 3. Average Delivery Time by Transportation Mode
    plt.figure(figsize=(9, 5))
    mode_time = df.groupby('transportation_mode')['actual_delivery_days'].mean().reset_index().sort_values(by='actual_delivery_days')
    bars = plt.bar(mode_time['transportation_mode'], mode_time['actual_delivery_days'], color='#34495e', width=0.5, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.2f} days',
                 ha='center', va='bottom', fontweight='bold')
    plt.title("Average Delivery Duration by Transportation Mode", pad=15)
    plt.xlabel("Transportation Mode")
    plt.ylabel("Average Delivery Time (Days)")
    plt.ylim(0, max(mode_time['actual_delivery_days']) * 1.15)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "avg_delivery_time_by_mode.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)
    
    # 4. Average Delay by Weather Condition
    plt.figure(figsize=(9, 5))
    weather_delay = df.groupby('weather_condition')['delay_days'].mean().reset_index().sort_values(by='delay_days', ascending=False)
    bars = plt.bar(weather_delay['weather_condition'], weather_delay['delay_days'], color='#e67e22', width=0.5, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05, f'{height:.2f} days',
                 ha='center', va='bottom', fontweight='bold')
    plt.title("Impact of Weather Condition on Average Delivery Delay", pad=15)
    plt.xlabel("Weather Condition")
    plt.ylabel("Average Delay (Days)")
    plt.ylim(0, max(weather_delay['delay_days']) * 1.2)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "delay_by_weather.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)
    
    # 5. Cost Analysis: Shipping Cost Distribution
    plt.figure(figsize=(9, 5))
    sns.histplot(df['shipping_cost'], bins=25, kde=True, color='#27ae60', edgecolor='black', alpha=0.6)
    plt.title("Distribution of Transportation Shipping Costs", pad=15)
    plt.xlabel("Shipping Cost ($)")
    plt.ylabel("Number of Shipments")
    plt.axvline(df['shipping_cost'].mean(), color='black', linestyle='--', linewidth=2, label=f"Mean Cost: ${df['shipping_cost'].mean():.2f}")
    plt.legend()
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "shipping_cost_distribution.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 6. Cost by Transportation Mode
    plt.figure(figsize=(9, 5))
    sns.boxplot(x='transportation_mode', y='shipping_cost', hue='transportation_mode', data=df, palette="Set2", legend=False)
    plt.title("Shipping Cost Distribution by Transportation Mode", pad=15)
    plt.xlabel("Transportation Mode")
    plt.ylabel("Shipping Cost ($)")
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "cost_by_mode.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 7. Distance vs Shipping Cost (Scatter + Regression)
    plt.figure(figsize=(9, 5.5))
    sns.regplot(x='distance_km', y='shipping_cost', data=df,
                scatter_kws={'alpha': 0.4, 'color': '#2980b9'},
                line_kws={'color': '#c0392b', 'linewidth': 2.5})
    plt.title("Distance (km) vs Shipping Cost ($) Regression Analysis", pad=15)
    plt.xlabel("Distance (km)")
    plt.ylabel("Shipping Cost ($)")
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "cost_vs_distance.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 8. Warehouse Analysis: Orders by Warehouse
    plt.figure(figsize=(10, 5))
    wh_orders = df['warehouse'].value_counts().reset_index()
    wh_orders.columns = ['warehouse', 'count']
    bars = plt.barh(wh_orders['warehouse'], wh_orders['count'], color='#16a085', edgecolor='black', alpha=0.85)
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 5, bar.get_y() + bar.get_height()/2., f'{width}',
                 ha='left', va='center', fontweight='bold')
    plt.title("Shipment Volume Handled per Warehouse Hub", pad=15)
    plt.xlabel("Total Order / Shipment Volume")
    plt.ylabel("Warehouse Location")
    plt.xlim(0, max(wh_orders['count']) * 1.15)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "orders_by_warehouse.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 9. Warehouse Utilization Rate
    plt.figure(figsize=(10, 5))
    wh_util = df.groupby('warehouse')['warehouse_utilization'].mean().reset_index().sort_values(by='warehouse_utilization', ascending=False)
    bars = plt.bar(wh_util['warehouse'], wh_util['warehouse_utilization'], color='#8e44ad', width=0.5, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%',
                 ha='center', va='bottom', fontweight='bold')
    plt.title("Average Capacity Utilization Rate by Warehouse", pad=15)
    plt.xlabel("Warehouse Location")
    plt.ylabel("Capacity Utilization (%)")
    plt.axhline(80.0, color='red', linestyle=':', label='Target Threshold (80%)')
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "warehouse_utilization.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 10. Warehouse Performance Comparison (On-Time Rate vs Avg Delay)
    plt.figure(figsize=(10, 5))
    wh_perf = df.groupby('warehouse').agg(
        on_time_rate=('is_on_time', lambda x: round(x.mean() * 100, 1)),
        avg_cost=('shipping_cost', 'mean')
    ).reset_index()
    
    x = np.arange(len(wh_perf['warehouse']))
    width = 0.35
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    rects1 = ax1.bar(x - width/2, wh_perf['on_time_rate'], width, label='On-Time Delivery Rate (%)', color='#2ecc71', edgecolor='black')
    rects2 = ax2.bar(x + width/2, wh_perf['avg_cost'], width, label='Average Cost ($)', color='#3498db', edgecolor='black')
    
    ax1.set_xlabel('Warehouse')
    ax1.set_ylabel('On-Time Delivery Rate (%)', color='#2ecc71', fontweight='bold')
    ax2.set_ylabel('Average Shipping Cost ($)', color='#3498db', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(wh_perf['warehouse'], rotation=15, ha='right')
    ax1.set_ylim(0, 110)
    ax2.set_ylim(0, max(wh_perf['avg_cost']) * 1.25)
    
    plt.title("Warehouse Comparative Performance: On-Time Rate vs Average Cost", pad=15)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "warehouse_performance_comparison.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 11. Geographic/Route Analysis: Top 10 Routes by Delay
    plt.figure(figsize=(10, 5.5))
    route_delay = df.groupby('route')['delay_days'].mean().nlargest(10).reset_index().sort_values(by='delay_days')
    bars = plt.barh(route_delay['route'], route_delay['delay_days'], color='#d35400', edgecolor='black', alpha=0.85)
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height()/2., f'{width:.2f} days',
                 ha='left', va='center', fontweight='bold')
    plt.title("Top 10 Origin-Destination Routes with Highest Delivery Delays", pad=15)
    plt.xlabel("Average Delay Duration (Days)")
    plt.ylabel("Origin -> Destination Route")
    plt.xlim(0, max(route_delay['delay_days']) * 1.2)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "top_routes_delay.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 12. Geographic/Route Analysis: Top 10 Routes by Cost
    plt.figure(figsize=(10, 5.5))
    route_cost = df.groupby('route')['shipping_cost'].mean().nlargest(10).reset_index().sort_values(by='shipping_cost')
    bars = plt.barh(route_cost['route'], route_cost['shipping_cost'], color='#2980b9', edgecolor='black', alpha=0.85)
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 20, bar.get_y() + bar.get_height()/2., f'${width:.2f}',
                 ha='left', va='center', fontweight='bold')
    plt.title("Top 10 Origin-Destination Routes with Highest Average Shipping Cost", pad=15)
    plt.xlabel("Average Shipping Cost ($)")
    plt.ylabel("Origin -> Destination Route")
    plt.xlim(0, max(route_cost['shipping_cost']) * 1.18)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "top_routes_cost.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 13. Product Analysis: Orders by Product Category
    plt.figure(figsize=(9, 5))
    prod_orders = df['product_category'].value_counts()
    bars = plt.bar(prod_orders.index, prod_orders.values, color='#16a085', width=0.5, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5, f'{height}',
                 ha='center', va='bottom', fontweight='bold')
    plt.title("Order Volume Distribution by Product Category", pad=15)
    plt.xlabel("Product Category")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=15, ha='right')
    plt.ylim(0, max(prod_orders.values) * 1.15)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "orders_by_product_category.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    # 14. Correlation Heatmap
    plt.figure(figsize=(10, 7))
    num_cols = ['distance_km', 'quantity', 'order_value', 'shipping_cost', 
                'estimated_delivery_days', 'actual_delivery_days', 'delay_days', 
                'fuel_cost', 'warehouse_utilization', 'is_delayed']
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title("Logistics Numerical Feature Correlation Matrix", pad=15)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    saved_charts.append(chart_path)

    print(f"EDA Visualization Suite Successfully Generated: {len(saved_charts)} charts saved in {output_dir}")
    return saved_charts

if __name__ == "__main__":
    from data_cleaning import load_raw_data, clean_and_prepare_data
    df = clean_and_prepare_data(load_raw_data())
    run_eda(df)
