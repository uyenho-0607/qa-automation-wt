import random

import pytest

from src.apis.api_client import APIClient
from src.data.consts import SYMBOLS
from src.data.enums import OrderType, AccSummary
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import ProjectConfig
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, setup):
    exp_account_summary, acc_details = setup

    logger.info("Step 1: Open My Account modal")
    android.home_screen.open_my_account()

    logger.info("Verify account summary against api data")
    android.home_screen.my_account_modal.verify_account_info(exp_account_summary)

    logger.info("Step 2: Close My Account modal")
    android.home_screen.my_account_modal.close()

    logger.info(f"Verify Available Account = {exp_account_summary.get(AccSummary.BALANCE)}")
    android.home_screen.verify_available_account(exp_account_summary)


@pytest.fixture
def setup(android):
    logger.info("- Place order to make sure account has Margin Level")
    trade_object = ObjTrade(order_type=OrderType.MARKET)
    APIClient().trade.post_order(trade_object)

    account_summary = APIClient().statistics.get_account_statistics(get_acc_balance=True)
    account_details = APIClient().user.get_user_account()

    yield account_summary, account_details
    logger.info("- Close My Account modal")
    android.home_screen.my_account_modal.close()
