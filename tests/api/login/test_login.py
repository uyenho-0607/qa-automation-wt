import pytest

from src.apis.api_client import APIClient
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

@pytest.mark.parametrize("times", range(20))
def test(times):
    logger.info("Step: Send API login to client")
    APIClient()


@pytest.fixture(autouse=True)
def cleanup():
    yield
    RuntimeConfig.headers = {}