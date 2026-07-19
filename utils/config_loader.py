import yaml
from utils.constants import AppConstants
from utils.file_handler import resource_path  # adjust import if resource_path lives elsewhere

class ConfigLoader:
    """Load application settings from YAML."""

    @staticmethod
    def load() -> dict:
        try:
            cfg_path = resource_path(*AppConstants.CONFIG_FILE)
            with open(cfg_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except Exception:
            return {}
