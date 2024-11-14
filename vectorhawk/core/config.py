import os
from dotenv import load_dotenv
from vectorhawk.core.logger import get_logger

# Load environment variables from a .env file
load_dotenv()

# Get the logger instance
logger = get_logger("vectorhawk")


class Config:
    """Configuration settings for VectorHawk."""

    def __init__(self):
        # Elasticsearch Configuration
        es_host = os.getenv("ES_HOST")
        if not es_host:
            logger.error("Elasticsearch host (ES_HOST) is not set.")
            raise ValueError("Elasticsearch host (ES_HOST) is not set.")
        self.ES_HOST = es_host.rstrip("/")  # Standardize without trailing slash

        self.ES_USER = os.getenv("ES_USER")
        self.ES_PASSWORD = os.getenv("ES_PASSWORD")
        if self.ES_USER and not self.ES_PASSWORD:
            logger.error("ES_USER is set but ES_PASSWORD is missing.")
            raise ValueError("ES_USER is set but ES_PASSWORD is missing.")

        # LLM Server Configuration
        self.LLM_MODEL = os.getenv(
            "LLM_MODEL", "mistral-7b"
        )  # Default model set to Mistral 7B
        try:
            self.LLM_API_PORT = int(os.getenv("LLM_API_PORT", 8000))
        except ValueError:
            logger.error("LLM_API_PORT must be an integer.")
            raise ValueError("LLM_API_PORT must be an integer.")

        # General Configuration
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ["true", "1", "t"]
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_DIR = os.getenv("LOG_DIR", "./logs")

        logger.info(
            "Configuration initialized successfully with given environment variables."
        )


# Optional: Add a function to validate the configuration if needed.
# def validate_config(config):
#     if not config.ES_HOST:
#         logger.error("Elasticsearch host (ES_HOST) is not set.")
#         raise ValueError("Elasticsearch host (ES_HOST) is not set.")

#     if config.ES_USER and not config.ES_PASSWORD:
#         logger.error("ES_USER is set but ES_PASSWORD is missing.")
#         raise ValueError("ES_USER is set but ES_PASSWORD is missing.")
