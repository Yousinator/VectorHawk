import logging
import os
from logging.handlers import RotatingFileHandler

# Directory to store logs
LOG_DIR = os.getenv("LOG_DIR", "./logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Create the directory if it doesn't exist

LOG_FILE_PATH = os.path.join(LOG_DIR, "vectorhawk.log")

# Configure logging to file with rotation
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=3
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Set up stream handler for console logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,  # Default log level
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger("vectorhawk")


def get_logger(name: str = "vectorhawk"):
    """Returns a logger instance."""
    return logging.getLogger(name)
