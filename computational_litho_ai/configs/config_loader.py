import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

# Load from .env
load_dotenv()

CONFIG_PATH = Path(__file__).parent / "model_config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    # Use OPENAI_API_KEY from .env if available
    env_api_key = os.getenv("OPENAI_API_KEY")
    if env_api_key:
        config["auth"]["openai_api_key"] = env_api_key
    elif not config["auth"]["openai_api_key"]:
        raise ValueError("OPENAI_API_KEY not found in .env or YAML.")

    return config

config = load_config()
