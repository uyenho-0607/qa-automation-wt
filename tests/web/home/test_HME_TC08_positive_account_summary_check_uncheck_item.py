import random

import pytest
from src.utils.logging_utils import logger
from src.data.enums import AccSummary


pytestmark = [pytest.mark.critical]


@pytest.mark.parametrize("account_item", AccSummary.checkbox_list())
def test_single_item(web, account_item):

    logger.info(f"Step 1: Uncheck: {account_item.value!r}")
    web.home_page.check_uncheck_balance_items(account_item, check=False)

    logger.info(f"Verify {account_item.value!r} is not displayed")
    web.home_page.verify_acc_balance_items_displayed(account_item, is_display=False)

    logger.info(f"Step 2: Check {account_item.value!r}")
    web.home_page.check_uncheck_balance_items(account_item)

    logger.info(f"Verify {account_item.value!r} is displayed")
    web.home_page.verify_acc_balance_items_displayed(account_item)


def test_multiple_items(web):
    items = random.sample(AccSummary.checkbox_list(), 4)
    display_logs = ', '.join(item.value for item in items)

    logger.info(f"Step 1: Uncheck: {display_logs}")
    web.home_page.check_uncheck_balance_items(items, check=False)

    logger.info(f"Verify {display_logs} is not displayed")
    web.home_page.verify_acc_balance_items_displayed(items, is_display=False)

    logger.info(f"Step 2: Check: {display_logs}")
    web.home_page.check_uncheck_balance_items(items, check=True)

    logger.info(f"Verify {display_logs} is displayed")
    web.home_page.verify_acc_balance_items_displayed(items)


@pytest.fixture(autouse=True)
def teardown(web):
    yield
    logger.info("- Show all account summary items")
    web.home_page.check_uncheck_balance_items(AccSummary.checkbox_list())

