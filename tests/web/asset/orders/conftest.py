import pytest

from src.data.enums import Features
from src.utils.logging_utils import logger


@pytest.fixture(autouse=True, scope="package")
def disable_OCT(disable_OCT, web):
    logger.info("- Navigate to Assets Page")
    web.home_page.navigate_to(Features.ASSETS)
