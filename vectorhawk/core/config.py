import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """Configuration settings for VectorHawk."""

    # Elasticsearch Configuration
    ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
    ES_USER = os.getenv("ES_USER", "")
    ES_PASSWORD = os.getenv("ES_PASSWORD", "")

    # LLM Server Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "mistral-7b")  # Default model set to Mistral 7B
    LLM_API_PORT = os.getenv("LLM_API_PORT", 8000)


    # General Configuration
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ['true', '1', 't']
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
