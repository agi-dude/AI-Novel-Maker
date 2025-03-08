import os
from pathlib import Path

# Base directories
# BASE_DIR = Path(__file__).resolve().parent
BASE_DIR = Path("./output/")
LOGS_DIR = BASE_DIR / "logs"
SAVE_DIR = BASE_DIR / "saves"

# Ensure directories exist
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SAVE_DIR, exist_ok=True)

# Ollama settings
DEFAULT_MODEL = "mistral-nemo"  # Default model to use
OLLAMA_API_HOST = "http://localhost:11434"  # Ollama API host

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Application settings
HEADLESS_MODE = False  # Set to True to run without user interaction
MAX_CHAPTERS = 25  # Maximum number of chapters to generate
