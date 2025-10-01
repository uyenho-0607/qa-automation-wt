from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


def test():
    logger.debug("Step: Send API login to client")
    APIClient()