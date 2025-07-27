from pathlib import Path
import os

APP_VERIONS = "3.1.0"
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_LOCATION = Path(os.environ.get("SOUNDBOARD_CONFIG_LOCATION", "./config.toml"))