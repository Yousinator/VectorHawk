from vectorhawk.core.logger import get_logger

# Initialize logger for exceptions
logger = get_logger(__name__)


class VectorHawkError(Exception):
    """Base class for all custom exceptions in VectorHawk."""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred in VectorHawk."
        super().__init__(message)
        logger.error(message)  # Automatically log the error when raised


class ElasticsearchError(VectorHawkError):
    """Exception raised for errors related to Elasticsearch."""

    def __init__(self, message="Error interacting with Elasticsearch"):
        super().__init__(message)
        logger.error(message)  # Log the specific Elasticsearch error


class ConfigError(VectorHawkError):
    """Exception raised for configuration-related issues."""

    def __init__(self, message="Configuration error in VectorHawk"):
        super().__init__(message)
        logger.error(message)  # Log the specific configuration error
