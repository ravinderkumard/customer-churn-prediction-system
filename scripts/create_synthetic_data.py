# scripts/create_synthetic_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yaml
import os
import sys

print(" Customer Churn Synthetic Data Generator")
print("=" * 60)

class Config:
    """Simple configuration loader"""
    
    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load config from YAML file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            print(f" Loaded config from: {self.config_path}")
            return config
        else:
            print(f"Config file not found: {self.config_path}")
            print("Using default configuration...")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Return default configuration"""
        return {
            'project': {
                'name': 'customer-churn-predictor',
                'version': '1.0.0'
            },
            'data': {
                'raw_dir': 'data/raw',
                'num_customers': 1000,
                'start_date': '2022-01-01',
                'end_date': '2023-12-31',
                'files': {
                    'customers': 'customers.csv',
                    'transactions': 'transactions.csv',
                    'support_calls': 'support_calls.csv',
                    'usage_data': 'usage_data.csv',
                    'churn_target': 'churn_target.csv'
                }
            },
            'synthetic_data': {
                'customers': {
                    'age': {'min': 18, 'max': 75, 'mean': 42, 'std': 12},
                    'income_segments': {'Low': 0.3, 'Medium': 0.5, 'High': 0.2},
                    'regions': ['North', 'South', 'East', 'West'],
                    'contract_types': {
                        'Monthly': {'probability': 0.6},
                        'Annual': {'probability': 0.3},
                        'TwoYear': {'probability': 0.1}
                    }
                }
            },
            'random': {
                'seed': 42
            }
        }
    
    def get(self, key, default=None):
        """Get value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

def generate_customers():
    """Generate synthetic customer data"""
    print("\n Generating customer data...")
    
    # Load config
    config = Config()
    
    # Set random seed
    seed = config.get('random.seed', 42)
    np.random.seed(seed)
    print(f"Random seed: {seed}")
    
    # Get number of customers
    n_customers = config.get('data.num_customers', 1000)
    print(f"Number of customers: {n_customers}")
    
    # Create customer IDs
    customer_ids = [f'CUST{str(i).zfill(6)}' for i in range(1, n_customers + 1)]
    
    # Generate signup dates
    start_date = datetime.strptime(
        config.get('data.start_date', '2022-01-01'), 
        '%Y-%m-%d'
    )
    end_date = datetime.strptime(
        config.get('data.end_date', '2023-12-31'), 
        '%Y-%m-%d'
    )
    date_range = (end_date - start_date).days
    
    # Generate ages
    age_config = config.get('synthetic_data.customers.age', {'min': 18, 'max': 75, 'mean': 42, 'std': 12})
    ages = np.random.normal(age_config['mean'], age_config['std'], n_customers)
    ages = np.clip(ages, age_config['min'], age_config['max']).astype(int)
    
    # Generate income segments
    income_segments = config.get('synthetic_data.customers.income_segments', {'Low': 0.3, 'Medium': 0.5, 'High': 0.2})
    segment_names = list(income_segments.keys())
    segment_probs = list(income_segments.values())
    
    # Generate regions
    regions = config.get('synthetic_data.customers.regions', ['North', 'South', 'East', 'West'])
    
    # Generate contract types
    contract_types = config.get('synthetic_data.customers.contract_types', {
        'Monthly': {'probability': 0.6},
        'Annual': {'probability': 0.3},
        'TwoYear': {'probability': 0.1}
    })
    contract_names = list(contract_types.keys())
    contract_probs = [ct['probability'] for ct in contract_types.values()]
    
    # Create DataFrame
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'signup_date': [
            (start_date + timedelta(days=np.random.randint(0, date_range))).date()
            for _ in range(n_customers)
        ],
        'age': ages,
        'income_segment': np.random.choice(segment_names, size=n_customers, p=segment_probs),
        'region': np.random.choice(regions, size=n_customers),
        'contract_type': np.random.choice(contract_names, size=n_customers, p=contract_probs)
    })
    
    print(f" Generated {len(customers_df)} customer records")
    return customers_df

def generate_transactions(customers_df):
    """Generate transaction data"""
    print("\n Generating transaction data...")
    
    config = Config()
    transactions = []
    
    for idx, customer in customers_df.iterrows():
        # Each customer has 5-50 transactions
        n_transactions = np.random.randint(5, 50)
        
        # Generate transaction dates
        signup_date = customer['signup_date']
        if isinstance(signup_date, str):
            signup_date = datetime.strptime(signup_date, '%Y-%m-%d').date()
        
        end_date = datetime.strptime(
            config.get('data.end_date', '2023-12-31'), 
            '%Y-%m-%d'
        ).date()
        
        date_range = (end_date - signup_date).days
        if date_range > 0:
            for i in range(n_transactions):
                days_after = np.random.randint(0, date_range)
                tx_date = signup_date + timedelta(days=days_after)
                
                # Generate amount
                amount = np.random.uniform(10, 500)
                
                # Transaction type
                tx_types = ['subscription', 'purchase', 'refund', 'fee']
                tx_type = np.random.choice(tx_types, p=[0.6, 0.3, 0.05, 0.05])
                
                transactions.append({
                    'transaction_id': f'TX{len(transactions):08d}',
                    'customer_id': customer['customer_id'],
                    'date': tx_date,
                    'amount': round(amount, 2),
                    'type': tx_type
                })
    
    transactions_df = pd.DataFrame(transactions)
    print(f" Generated {len(transactions_df)} transaction records")
    return transactions_df

def save_data(df, filename):
    """Save DataFrame to CSV"""
    config = Config()
    raw_dir = config.get('data.raw_dir', 'data/raw')
    
    # Create directory if it doesn't exist
    os.makedirs(raw_dir, exist_ok=True)
    
    filepath = os.path.join(raw_dir, filename)
    df.to_csv(filepath, index=False)
    print(f" Saved to: {filepath}")
    
    return filepath

def main():
    """Main function to generate all data"""
    print("\n" + "=" * 60)
    print(" DATA GENERATION STARTING")
    print("=" * 60)
    
    # Generate customers
    customers_df = generate_customers()
    
    # Generate transactions
    transactions_df = generate_transactions(customers_df)
    
    # Save data
    print("\n Saving data to files...")
    customers_file = save_data(customers_df, 'customers.csv')
    transactions_file = save_data(transactions_df, 'transactions.csv')
    
    # Create simple support_calls and usage_data
    print("\n Generating support calls data...")
    support_calls_df = pd.DataFrame({
        'customer_id': np.random.choice(customers_df['customer_id'], 1000),
        'date': pd.date_range(start='2023-01-01', periods=1000, freq='D').date,
        'issue_type': np.random.choice(['technical', 'billing', 'account', 'other'], 1000),
        'duration_minutes': np.random.randint(2, 30, 1000),
        'resolved': np.random.choice([True, False], 1000, p=[0.8, 0.2])
    })
    save_data(support_calls_df, 'support_calls.csv')
    
    print("\n Generating usage data...")
    usage_df = pd.DataFrame({
        'customer_id': np.random.choice(customers_df['customer_id'], 5000),
        'date': pd.date_range(start='2023-06-01', periods=5000, freq='D').date,
        'minutes_used': np.random.randint(0, 240, 5000),
        'features_accessed': np.random.randint(1, 10, 5000),
        'sessions': np.random.randint(1, 20, 5000)
    })
    save_data(usage_df, 'usage_data.csv')
    
    print("\n" + "=" * 60)
    print(" DATA GENERATION COMPLETED!")
    print("=" * 60)
    
    # Show summary
    print("\n DATA SUMMARY:")
    print("-" * 30)
    print(f"Customers: {len(customers_df)}")
    print(f"Transactions: {len(transactions_df)}")
    print(f"Support Calls: {len(support_calls_df)}")
    print(f"Usage Records: {len(usage_df)}")
    
    # Show sample
    print("\n  SAMPLE DATA (First 3 rows):")
    print("-" * 30)
    print("Customers:")
    print(customers_df.head(3))
    print("\nTransactions:")
    print(transactions_df.head(3))

if __name__ == "__main__":
    main()