# test_config.py (place in project root)
import yaml
import os
import sys

print("🔧 Testing Configuration System")
print("=" * 50)

def test_config():
    """Simple test of the configuration system"""
    
    # 1. Check if config file exists
    config_path = "config/config.yaml"
    
    if not os.path.exists(config_path):
        print(f" Config file not found at: {config_path}")
        print("Creating default config file...")
        
        # Create config directory if it doesn't exist
        os.makedirs("config", exist_ok=True)
        
        # Create default config
        default_config = {
            'project': {
                'name': 'customer-churn-predictor',
                'version': '1.0.0'
            },
            'data': {
                'raw_dir': 'data/raw',
                'num_customers': 1000
            }
        }
        
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        print(f" Created default config at: {config_path}")
    
    # 2. Load the config
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f" Successfully loaded config from: {config_path}")
        
        # 3. Test accessing values
        print("\n Config Values:")
        print("-" * 30)
        
        # Safe way to get nested values
        def get_nested(config_dict, keys, default=None):
            """Get nested value from dictionary"""
            value = config_dict
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            return value
        
        # Get values with fallbacks
        project_name = get_nested(config, ['project', 'name'], 'Unknown')
        num_customers = get_nested(config, ['data', 'num_customers'], 1000)
        seed = get_nested(config, ['random', 'seed'], 42)
        
        print(f"Project Name: {project_name}")
        print(f"Number of Customers: {num_customers}")
        print(f"Random Seed: {seed}")
        
        # 4. Test data directory
        raw_dir = get_nested(config, ['data', 'raw_dir'], 'data/raw')
        os.makedirs(raw_dir, exist_ok=True)
        print(f"Data Directory: {raw_dir} (exists: {os.path.exists(raw_dir)})")
        
        # 5. Print full config
        print("\n Full Config Structure:")
        print("-" * 30)
        print(yaml.dump(config, default_flow_style=False))
        
        return True
        
    except Exception as e:
        print(f" Error loading config: {e}")
        return False

def test_simple_config_class():
    """Test a simple config class"""
    print("\n" + "=" * 50)
    print(" Testing SimpleConfig Class")
    print("=" * 50)
    
    class SimpleConfig:
        """Simple configuration loader without external dependencies"""
        
        def __init__(self, config_path="config/config.yaml"):
            self.config_path = config_path
            self.config = self._load_config()
        
        def _load_config(self):
            """Load config from YAML file"""
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                print(f"Config file not found: {self.config_path}")
                return {}
        
        def get(self, key, default=None):
            """Get value using dot notation: 'data.num_customers'"""
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        
        def get_path(self, *args):
            """Get absolute path for files"""
            return os.path.join(os.getcwd(), *args)
    
    # Create and test the config
    config = SimpleConfig()
    
    print(f"Config loaded: {config.config_path}")
    print(f"Project: {config.get('project.name')}")
    print(f"Customers: {config.get('data.num_customers', 1000)}")
    print(f"Raw path: {config.get_path('data', 'raw')}")
    
    print("\n SimpleConfig test completed!")

def main():
    """Main test function"""
    print(" Customer Churn Config Test")
    print("=" * 50)
    
    # Test 1: Direct config loading
    if test_config():
        print("\n All config tests passed!")
    
    # Test 2: SimpleConfig class
    test_simple_config_class()
    
    print("\n" + "=" * 50)
    print(" SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Generate data: python scripts/create_synthetic_data.py")
    print("3. Explore data: jupyter notebook notebooks/01_eda.ipynb")

if __name__ == "__main__":
    main()