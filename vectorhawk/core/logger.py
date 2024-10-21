import logging
import os
from vectorhawk.core.config import config

# Directory to store logs
LOG_DIR = os.getenv("LOG_DIR", "./logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Create the directory if it doesn't exist

LOG_FILE_PATH = os.path.join(LOG_DIR, "vectorhawk.log")

# Configure logging to file
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, config.LOG_LEVEL.upper(), "INFO"),
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger("vectorhawk")

def get_logger(name: str = "vectorhawk"):
    """Returns a logger instance."""
    return logging.getLogger(name)
