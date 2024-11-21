import yaml
from typing import Dict, Any
from pathlib import Path

class Config:
    def __init__(self, config_path: str):
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_env_config(self) -> Dict[str, Any]:
        return self.config.get('environment', {})

    def get_agent_configs(self) -> Dict[str, Any]:
        return self.config.get('agents', [])

    def get_policy_configs(self) -> Dict[str, Any]:
        return self.config.get('policies', {}) 