# Smart Logistics Performance & Delivery Optimization Analytics

**Week 1 Project: Strategic Planning and Data Exploration in Logistics**  
**Role:** Logistics Data Analyst Intern  
**Domain:** Supply Chain & Freight Operations Analytics  

---

## 📌 Project Overview

This repository contains the complete, submission-ready project for **Week 1 of the 4-Week Logistics Data Analyst Internship**. 

The project, titled **"Smart Logistics Performance & Delivery Optimization Analytics"**, addresses critical real-world logistics challenges faced by supply chain enterprises: freight delivery delays, high transportation expenses, suboptimal warehouse capacity utilization, and unpredictable transit times across multi-city delivery networks.

Using Python data science libraries (**Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn**), this project executes raw data cleaning, derived feature engineering, KPI formulation, exploratory visual analysis, predictive machine learning modeling (Regression & Classification), and K-Means shipment segmentation.

---

## 🎯 Business Problem & Key Objectives

### Business Problem
A multi-hub logistics company delivers merchandise from **5 central warehouse distribution hubs** to customers across **10 major urban destinations**. Operational bottlenecks include:
- **39.9% Delivery Delay Rate** leading to customer dissatisfaction and SLA penalties.
- High average shipping cost ($1,145.91/shipment) driven by distance and air cargo usage.
- Uneven warehouse workload and inventory capacity imbalance.
- Lack of early warning delay prediction models.

### Key Objectives
1. **Elevate On-Time Delivery Rate** from ~60% to >90%.
2. **Reduce Average Transportation Costs** by 12–15% via modal optimization.
3. **Identify High-Risk Bottleneck Routes** suffering chronic delays.
4. **Formulate 11 Core Logistics KPIs** for continuous tracking.
5. **Develop ML Delay Classifiers** with >75% accuracy to flag delay risks before dispatch.
6. **Segment Shipments** into distinct operational personas using K-Means clustering.
7. **Deliver a 4-Week Strategic Implementation Roadmap**.

---

## 📊 Logistics Key Performance Indicators (KPIs)

The project defines and calculates **11 primary & secondary Logistics KPIs**:

| KPI Category | KPI Name | Formula / Definition | Baseline Target | Project Value |
| :--- | :--- | :--- | :--- | :--- |
| **Service Quality** | **On-Time Delivery Rate** | `(On-Time Deliveries / Total Deliveries) * 100` | `> 92.0%` | `60.08%` |
| **Service Quality** | **Delivery Delay Rate** | `(Delayed Deliveries / Total Deliveries) * 100` | `< 8.0%` | `39.92%` |
| **Operational Speed** | **Average Delivery Time** | `Total Delivery Time / Total Shipments` | `< 3.5 days` | `6.99 days` |
| **Operational Speed** | **Average Delay Duration** | `Sum of Delay Days / Total Delayed Shipments` | `< 1.5 days` | `1.83 days` |
| **Cost Efficiency** | **Average Transportation Cost** | `Total Shipping Cost / Total Shipments` | `< $850.00` | `$1,145.91` |
| **Cost Efficiency** | **Cost per Shipment** | `Total Shipping Cost / Total Shipments` | `< $850.00` | `$1,145.91` |
| **Inventory & WH** | **Order Fulfillment Rate** | `(Fulfilled Orders / Total Orders) * 100` | `> 99.0%` | `98.65%` |
| **Inventory & WH** | **Inventory Turnover** | `Total Quantity Shipped / Mean Inventory Level` | `> 55.0x` | `47.88x` |
| **Inventory & WH** | **Warehouse Utilization** | `Mean (Inventory Level / Warehouse Capacity) * 100` | `75% - 85%` | `68.64%` |
| **Network & Route** | **Average Distance** | `Total Distance / Total Shipments` | `Network Metric` | `1,114.7 km` |
| **Network & Route** | **Route Efficiency Index** | `Mean (Distance / Actual Delivery Time)` | `> 300 km/day` | `233.1 km/day` |

---

## 📁 Project Folder Structure

```text
logistics-data-analytics/
│
├── data/
│   └── logistics_data.csv                   # Raw simulated logistics dataset (1,250 records)
│
├── notebooks/
│   └── logistics_analysis.ipynb              # Executable Jupyter Notebook with full analysis workflow
│
├── src/
│   ├── generate_dataset.py                   # Reproducible synthetic dataset generator (seed=42)
│   ├── data_cleaning.py                      # Data preparation & derived feature engineering engine
│   ├── kpi_analysis.py                       # KPI calculation & export script
│   ├── eda.py                                # Visual analysis & high-res chart generator
│   ├── prediction.py                         # Regression & Classification ML modeling engine
│   ├── clustering.py                         # K-Means segmentation & Elbow method module
│   ├── build_docx_report.py                  # DOCX Strategic Planning Report compiler
│   └── create_notebook.py                    # Programmatic Jupyter Notebook creator
│
├── outputs/
│   ├── charts/                               # 14 High-resolution EDA & ML charts (PNG)
│   │   ├── delivery_status_distribution.png
│   │   ├── delay_days_distribution.png
│   │   ├── avg_delivery_time_by_mode.png
│   │   ├── delay_by_weather.png
│   │   ├── shipping_cost_distribution.png
│   │   ├── cost_by_mode.png
│   │   ├── cost_vs_distance.png
│   │   ├── orders_by_warehouse.png
│   │   ├── warehouse_utilization.png
│   │   ├── warehouse_performance_comparison.png
│   │   ├── top_routes_delay.png
│   │   ├── top_routes_cost.png
│   │   ├── orders_by_product_category.png
│   │   ├── correlation_heatmap.png
│   │   ├── feature_importance.png
│   │   ├── confusion_matrix.png
│   │   ├── kmeans_elbow_curve.png
│   │   └── customer_clusters.png
│   ├── cleaned_data.csv                      # Cleaned dataset with derived features
│   └── kpi_summary.csv                       # Formatted KPI metric output summary
│
├── docs/
│   └── Strategic_Planning_Report.docx        # Primary submission-ready internship report (DOCX)
│
├── requirements.txt                          # Python dependencies list
├── README.md                                 # Comprehensive project documentation
└── main.py                                   # Master pipeline runner
```

---

## 🛠️ Technology Stack

- **Language:** Python 3.14+
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-Learn (Linear Regression, Random Forest, Logistic Regression, K-Means Clustering)
- **Document Processing:** python-docx, nbformat
- **Environment:** Jupyter Notebook, PowerShell / Command Line

---

## 🚀 Installation & Setup Instructions

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system.

### 2. Clone / Open Project Directory
Navigate to the project root:
```bash
cd logistics-data-analytics
```

### 3. Install Dependencies
Install all required Python packages via `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Project

### Option A: Run End-to-End Pipeline via `main.py` (Recommended)
To execute data loading, cleaning, KPI calculation, chart generation, ML training, and clustering in one command:

```bash
python main.py
```

### Option B: Build Primary Submission DOCX Report
To compile the formal submission report (`docs/Strategic_Planning_Report.docx`):

```bash
python src/build_docx_report.py
```

### Option C: Interactive Exploration in Jupyter Notebook
Launch Jupyter Notebook to interactively view code, charts, and markdown explanations:

```bash
jupyter notebook notebooks/logistics_analysis.ipynb
```

---

## 📈 Key Findings & Predictive Results

1. **On-Time Delivery Performance:**
   - **60.08% On-Time Deliveries**, **39.92% Delayed Deliveries**.
   - Primary delay causes: Adverse weather (Storms, Fog) and high-distance road transport.

2. **Cost Drivers:**
   - Shipping cost has a strong positive correlation with transit distance ($r = 0.89$).
   - Air Cargo exhibits the highest average shipping cost ($1,850+), while Rail Freight is most economical ($520 average).

3. **Predictive Machine Learning Evaluation:**
   - **Regression Target (`actual_delivery_days`):** Linear Regression achieved $R^2 = 0.891$ with MAE = 0.702 days.
   - **Classification Target (`is_delayed`):** Logistic Regression achieved **76.8% Accuracy**, 67.5% Precision, and **81.0% Recall**.

4. **K-Means Shipment Segmentation:**
   - **Cluster 0:** High-Cost Long-Haul Cargo (Avg Distance: 1,650 km, Avg Cost: $1,820)
   - **Cluster 1:** Standard Regional Freight (Avg Distance: 620 km, Avg Cost: $650)
   - **Cluster 2:** High-Value Express Deliveries (Avg Distance: 980 km, Avg Cost: $1,210)

---

## 🗓️ Four-Week Internship Implementation Roadmap

- **Week 1 (Current Deliverable):** Strategic Planning, Data Exploration, KPI Formulation, EDA, ML Prototypes, DOCX Strategic Report.
- **Week 2:** Advanced Data Cleaning, Outlier Treatment, Interactive PowerBI/Streamlit Dashboard.
- **Week 3:** Hyperparameter Tuning (XGBoost / RandomForest), Predictive Delay Alert API Prototype.
- **Week 4:** Linear Programming Route Optimization (SciPy/PuLP), Final Presentation Deck & Internship Evaluation Submission.

---

## 📄 Primary Submission File

The primary document for evaluation is located at:
`docs/Strategic_Planning_Report.docx`

---
*Created for Logistics Data Analyst Internship — Week 1 Project.*
#   W e e k - 1 - T a s k - S t r a t e g i c - P l a n n i n g - a n d - D a t a - E x p l o r a t i o n - i n - L o g i s t i c s  
 