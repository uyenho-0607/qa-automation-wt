import pytest

from src.utils.logging_utils import logger


def test(web):
    logger.info("Step: Open account info")
    web.home_page.toggle_account_selector()

    logger.info("Verify account total balance")
    web.home_page.verify_acc_total_balance()


@pytest.fixture(autouse=True)
def cleanup(web):
    yield
    web.home_page.toggle_account_selector(open=False)
