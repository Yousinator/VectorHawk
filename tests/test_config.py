import os
print(os.getcwd())

from vectorhawk.core.config import config
from vectorhawk.core.logger import get_logger

logger = get_logger()

def test_config():
    logger.debug(f"Elasticsearch Host: {config.ES_HOST}")
    logger.debug(f"Elasticsearch User: {config.ES_USER}")
    logger.debug(f"LLM Model: {config.LLM_MODEL}")
    logger.debug(f"Debug Mode: {config.DEBUG_MODE}")
    logger.info("Core configuration is working as expected!")

if __name__ == "__main__":
    test_config()
