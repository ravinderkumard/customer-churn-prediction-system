# Customer Churn Prediction System

## Business Problem

A telecom company is losing 2.5% of its monthly subscriber base to competitors, costing approximately $3M monthly in lost revenue. The current reactive approach (offering discounts only when customers call to cancel) is ineffective and expensive. The goal is to proactively identify customers likely to churn and implement retention strategies to reduce churn rates, thereby saving costs and improving customer satisfaction.

## Solution Value Proposition
By implementing a predictive churn model, the telecom company can identify at-risk customers before they decide to leave. This proactive approach allows for targeted retention efforts, such as personalized offers or improved customer service, which can significantly reduce churn rates. The anticipated benefits include:
- Reduction in monthly churn rate from 2.5% to 1.5%
- Monthly savings of approximately $1.2M in lost revenue
- Enhanced customer satisfaction and loyalty through personalized engagement
- Improved marketing efficiency by focusing retention efforts on high-risk customers

## Project Overview
This project involves developing a machine learning model to predict customer churn based on historical data. The model will analyze various customer attributes and behaviors to identify patterns associated with churn. The key steps in the project include:
1. Data Collection: Gather historical customer data, including demographics, service usage, billing information, and customer service interactions.
2. Data Preprocessing: Clean and preprocess the data to handle missing values, outliers, and categorical variables.
3. Exploratory Data Analysis (EDA): Analyze the data to identify trends, correlations, and important features related to churn.
4. Model Development: Train and evaluate various machine learning algorithms to identify the best-performing model for churn prediction.
5. Model Deployment: Implement the model in a production environment to provide real-time churn predictions.
6. Monitoring and Maintenance: Continuously monitor the model's performance and update it as needed to ensure accuracy over time.

## Solution Value Proposition
Build a predictive system that:
- Identifies at-risk customers 30 days before they churn
- Prioritizes retention efforts based on customer value and churn probability
- Automates personalized retention offers (discounts, upgrades, special plans)
- Tracks ROI of retention campaigns


## Day-to-Day Activities
### Day 1-2: Setup
- Set up project repository and environment
- Define requirements.txt file
- Define Business Understanding and Data Understanding documents

### Day 3: Data Generation & Configuration System
```
customer-churn-prediction-system/
├── config/ # Configuration files
│ └── config.yaml # Centralized project settings
├── data/ # Data storage
│ ├── raw/ # Raw synthetic data
├── scripts/ # Python scripts
│ ├── create_synthetic_data.py
│ └── test_config.py
├── requirements.txt # Python dependencies
└── README.md # This file
```

#### **2. Configuration System Implemented**
Created a flexible YAML-based configuration system that allows us to:

- **Centralize all project settings** in one file
- **Easily modify parameters** without changing code
- **Ensure reproducibility** with fixed random seeds
- **Define data generation rules** for synthetic data

**Key Configuration Sections:**
```yaml
# config/config.yaml
project:              # Project metadata
data:                # Data paths and sizes
synthetic_data:      # Data generation rules
churn:              # Churn definition parameters
random:             # Random seed for reproducibility
```

#### **3. Synthetic Data Generation**
**Built a scalable data generator that creates:**
- Customer demographics (age, income, region, contract type)
- Transaction history (amounts, dates, types)
- Customer support interactions (call types, durations)
- Product usage patterns (daily usage, features accessed)

**Data Characteristics:**
- 10,000 customers (configurable)
- Realistic distributions based on business scenarios
- Temporal relationships between different data types
- Configurable churn rate (default: 20%)

**Data Generator Features:**
- Reproducible with fixed random seed (42)
- Temporal consistency across datasets
- Business logic embedded in data generation
- CSV output with proper formatting
