# src/config/config_loader.py
import yaml
import os
from typing import Dict, Any
from datetime import datetime
import logging
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0,project_root)

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Load and manage configuration from YAML file"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
        
    def _find_config_file(self) -> str:
        """Find config file in standard locations"""
        possible_paths = [
            "config/config.yaml",
            "config.yaml",
            "../config/config.yaml",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(
            "Configuration file not found. Please create config/config.yaml"
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            logger.info(f"Loaded configuration from {self.config_path}")
            return config
            
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise KeyError(f"Configuration key '{key}' not found")
    
    def get_path(self, *args) -> str:
        """Get absolute path for data files"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, *args)
    
    def save_default_config(self, path: str = "config/config.yaml"):
        """Save default configuration template"""
        default_config = self._get_default_config()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        logger.info(f"Saved default configuration to {path}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration template"""
        return {
            'project': {
                'name': 'customer-churn-predictor',
                'version': '1.0.0'
            },
            'data': {
                'raw_dir': 'data/raw',
                'num_customers': 1000
            }
        }

# Singleton instance
_config_instance = None

def get_config(config_path: str = None) -> ConfigLoader:
    """Get or create configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader(config_path)
    return _config_instance