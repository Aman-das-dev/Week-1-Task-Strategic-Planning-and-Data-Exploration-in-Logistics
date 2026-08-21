"""
Synthetic Logistics Dataset Generator
Project: Smart Logistics Performance & Delivery Optimization Analytics
Note: This script generates simulated logistics dataset (1,250 records) for Week 1 Internship Project.
"""

import numpy as np
import pandas as pd
import os

def generate_logistics_dataset(output_path="data/logistics_data.csv", num_records=1250, seed=42):
    np.random.seed(seed)
    
    # 1. Base Fields
    shipment_ids = [f"SHIP-{10000 + i}" for i in range(1, num_records + 1)]
    
    start_date = pd.to_datetime('2025-01-01')
    end_date = pd.to_datetime('2025-12-31')
    random_days = np.random.randint(0, (end_date - start_date).days, size=num_records)
    order_dates = [(start_date + pd.Timedelta(days=int(d))).strftime('%Y-%m-%d') for d in random_days]
    
    warehouses = ['WH-North-Delhi', 'WH-West-Mumbai', 'WH-South-Bengaluru', 'WH-East-Kolkata', 'WH-Central-Nagpur']
    wh_probs = [0.25, 0.25, 0.20, 0.15, 0.15]
    selected_warehouses = np.random.choice(warehouses, size=num_records, p=wh_probs)
    
    # Warehouse capacities fixed map
    capacity_map = {
        'WH-North-Delhi': 10000,
        'WH-West-Mumbai': 12000,
        'WH-South-Bengaluru': 8500,
        'WH-East-Kolkata': 7500,
        'WH-Central-Nagpur': 6000
    }
    
    origin_cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Kolkata', 'Nagpur']
    destination_cities = ['Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Indore', 'Patna', 'Bhopal', 'Coimbatore', 'Kochi', 'Chandigarh']
    
    # Mapping warehouse to origin city
    wh_origin_map = {
        'WH-North-Delhi': 'Delhi',
        'WH-West-Mumbai': 'Mumbai',
        'WH-South-Bengaluru': 'Bengaluru',
        'WH-East-Kolkata': 'Kolkata',
        'WH-Central-Nagpur': 'Nagpur'
    }
    origins = [wh_origin_map[w] for w in selected_warehouses]
    destinations = np.random.choice(destination_cities, size=num_records)
    
    product_categories = ['Electronics', 'Consumer Goods', 'Apparel', 'Industrial Equipment', 'Automotive Parts', 'Perishables']
    product_probs = [0.25, 0.25, 0.20, 0.12, 0.10, 0.08]
    selected_categories = np.random.choice(product_categories, size=num_records, p=product_probs)
    
    customer_segments = ['Enterprise', 'SMB', 'E-Commerce Retailer', 'Individual']
    selected_segments = np.random.choice(customer_segments, size=num_records, p=[0.35, 0.30, 0.25, 0.10])
    
    quantities = np.random.randint(10, 450, size=num_records)
    unit_prices = np.random.uniform(15, 250, size=num_records)
    order_values = np.round(quantities * unit_prices, 2)
    
    # Distance in km
    distances = np.random.randint(120, 2100, size=num_records)
    
    # Mode selection based on distance & category
    modes = ['Road Freight (Truck)', 'Rail Freight', 'Air Cargo', 'Express Courier']
    selected_modes = []
    for d, cat in zip(distances, selected_categories):
        if cat == 'Electronics' and d > 1000 and np.random.rand() > 0.4:
            selected_modes.append('Air Cargo')
        elif d > 1200 and np.random.rand() > 0.5:
            selected_modes.append('Rail Freight')
        elif np.random.rand() > 0.8:
            selected_modes.append('Express Courier')
        else:
            selected_modes.append('Road Freight (Truck)')
            
    # Base speeds & cost factors
    mode_speed = {
        'Air Cargo': 600, # km/day equivalent
        'Express Courier': 450,
        'Road Freight (Truck)': 250,
        'Rail Freight': 200
    }
    
    mode_cost_rate = {
        'Air Cargo': 2.2,
        'Express Courier': 1.8,
        'Road Freight (Truck)': 0.95,
        'Rail Freight': 0.65
    }
    
    fuel_costs = np.round(np.random.uniform(1.15, 1.75, size=num_records), 2)
    weather_conditions = np.random.choice(['Clear', 'Rainy', 'Foggy', 'Stormy', 'Severe Heat'], size=num_records, p=[0.55, 0.20, 0.12, 0.08, 0.05])
    
    # Estimated Delivery Days
    estimated_days = []
    for d, m in zip(distances, selected_modes):
        base_est = max(1, int(np.ceil(d / mode_speed[m]))) + np.random.randint(1, 3)
        estimated_days.append(base_est)
    estimated_days = np.array(estimated_days)
    
    # Delays influenced by weather, distance, mode
    weather_delay_impact = {
        'Clear': 0,
        'Rainy': 1,
        'Foggy': 2,
        'Stormy': 3,
        'Severe Heat': 1
    }
    
    actual_days = []
    delays = []
    statuses = []
    
    for est, w, m, d in zip(estimated_days, weather_conditions, selected_modes, distances):
        w_delay = weather_delay_impact[w] if np.random.rand() < 0.65 else 0
        rand_delay = np.random.choice([0, 0, 0, 1, 2, 4], p=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02])
        
        total_delay = w_delay + rand_delay
        act = est + total_delay
        
        if act == est:
            # 15% chance of early delivery
            if np.random.rand() < 0.15 and act > 1:
                act -= 1
                status = 'Early'
                delay = 0
            else:
                status = 'On-Time'
                delay = 0
        elif act < est:
            status = 'Early'
            delay = 0
        else:
            status = 'Delayed'
            delay = act - est
            
        actual_days.append(act)
        delays.append(delay)
        statuses.append(status)
        
    actual_days = np.array(actual_days)
    delays = np.array(delays)
    statuses = np.array(statuses)
    
    # Shipping Cost calculation ($)
    shipping_costs = []
    for dist, qty, mode, fuel in zip(distances, quantities, selected_modes, fuel_costs):
        base = dist * mode_cost_rate[mode] * 0.8
        weight_factor = qty * 0.45
        fuel_factor = fuel * 35
        noise = np.random.normal(20, 15)
        cost = max(80.0, np.round(base + weight_factor + fuel_factor + noise, 2))
        shipping_costs.append(cost)
    shipping_costs = np.array(shipping_costs)
    
    # Inventory Level & Capacity
    inventory_levels = []
    warehouse_capacities = []
    for wh in selected_warehouses:
        cap = capacity_map[wh]
        inv = int(np.random.uniform(0.45, 0.92) * cap)
        warehouse_capacities.append(cap)
        inventory_levels.append(inv)
        
    df = pd.DataFrame({
        'shipment_id': shipment_ids,
        'order_date': order_dates,
        'warehouse': selected_warehouses,
        'origin_city': origins,
        'destination_city': destinations,
        'product_category': selected_categories,
        'quantity': quantities,
        'order_value': order_values,
        'distance_km': distances,
        'transportation_mode': selected_modes,
        'shipping_cost': shipping_costs,
        'estimated_delivery_days': estimated_days,
        'actual_delivery_days': actual_days,
        'delivery_status': statuses,
        'delay_days': delays,
        'customer_segment': selected_segments,
        'inventory_level': inventory_levels,
        'warehouse_capacity': warehouse_capacities,
        'fuel_cost': fuel_costs,
        'weather_condition': weather_conditions
    })
    
    # Introduce raw data realistic flaws for cleaning demonstration
    # a. A few whitespace padded strings in destination_city and product_category
    df.loc[df.sample(20, random_state=1).index, 'destination_city'] = df.loc[df.sample(20, random_state=1).index, 'destination_city'] + " "
    df.loc[df.sample(15, random_state=2).index, 'product_category'] = " " + df.loc[df.sample(15, random_state=2).index, 'product_category']
    
    # b. A few missing values in weather_condition and fuel_cost
    df.loc[df.sample(12, random_state=3).index, 'weather_condition'] = np.nan
    df.loc[df.sample(8, random_state=4).index, 'fuel_cost'] = np.nan
    
    # c. A couple of duplicated rows
    duplicates = df.head(5).copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Synthetic dataset generated successfully with {len(df)} records at: {output_path}")

if __name__ == "__main__":
    generate_logistics_dataset()
