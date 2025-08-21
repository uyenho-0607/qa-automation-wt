import pytest

from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def login_WT_app(ios):
    breakpoint()

    is_logged_in = ios.home_screen.wait_for_loaded()
    if is_logged_in:
        return

    else:
        max_retries = 3

        logger.info("- Login to WT app")
        ios.login_screen.login()

        logger.info("- Wait for home screen loaded")

        while not ios.home_screen.wait_for_loaded() and max_retries:
            max_retries -= 1

            logger.info(f"- Login failed, retry again")
            ios.login_screen.login()
