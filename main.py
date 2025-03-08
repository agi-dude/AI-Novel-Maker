import logging
import sys

from src.user_interface import UserInterface
from src.ollama_client import OllamaClient
from config import LOGS_DIR, LOG_FORMAT, LOG_LEVEL, DEFAULT_MODEL

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOGS_DIR / "app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)  # Also output logs to console
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main program entry"""
    try:
        ollama_client = OllamaClient(model=DEFAULT_MODEL)
        ui = UserInterface(ollama_client)
        ui.run()
    except Exception as e:
        logger.error(f"Program error: {e}", exc_info=True)
        print(f"Program error: {e}")
    finally:
        logger.info("Program ended")

if __name__ == "__main__":
    main()
