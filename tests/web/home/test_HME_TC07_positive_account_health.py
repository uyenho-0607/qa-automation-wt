import random

import pytest

from src.apis.api_client import APIClient
from src.data.consts import SYMBOLS
from src.data.enums import AccSummary, OrderType
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_teardown):
    exp_account_summary, acc_details = setup_teardown

    logger.info("Step 1: Open account dropdown details")
    web.home_page.toggle_account_selector()

    logger.info("Verify account dropdown info")
    web.home_page.verify_account_dropdown_details(acc_details)

    logger.info("Step 2: Close account dropdown details")
    web.home_page.toggle_account_selector(open=False)

    logger.info("Verify account details")
    web.home_page.verify_account_details(acc_details)

    logger.info("Step 1: Toggle balance summary and show all account summary items")
    web.home_page.check_uncheck_balance_items(AccSummary.checkbox_list())

    logger.info("Verify Account Balance against API data")
    web.home_page.verify_acc_balance_value(AccSummary.BALANCE, exp_account_summary)

    logger.info("Verify Margin Used against API data")
    web.home_page.verify_acc_balance_value(AccSummary.MARGIN_USED, exp_account_summary)

    logger.info("Verify Margin Level against API data")
    web.home_page.verify_acc_balance_value(AccSummary.MARGIN_LEVEL, exp_account_summary, 0.01)

    logger.info("Verify Equity against API data")
    web.home_page.verify_acc_balance_value(AccSummary.EQUITY, exp_account_summary, 0.01)

    logger.info("Verify Profit/Loss against API data")
    web.home_page.verify_acc_balance_value(AccSummary.PROFIT_LOSS, exp_account_summary, 0.05)

    logger.info("Verify Free Margin against API data")
    web.home_page.verify_acc_balance_value(AccSummary.FREE_MARGIN, exp_account_summary, 0.01)

    logger.info("Step 2: Toggle balance summary")
    web.home_page.toggle_balance_summary()

    logger.info("Verify Account Summary against Account Dropdown")
    web.home_page.verify_acc_summary_dropdown()

    logger.info("Verify Account Note item against API data")
    web.home_page.verify_acc_note_values(exp_account_summary)


@pytest.fixture
def setup_teardown(web):

    if not web.home_page.is_account_traded():
        logger.info("- Place order to make sure account has Margin Level")
        trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=random.choice(SYMBOLS[ProjectConfig.client]))
        APIClient().trade.post_order(trade_object)

        logger.info("- Refresh Page to load data")
        web.home_page.refresh_page()

    account_summary = APIClient().statistics.get_account_statistics(get_acc_balance=True)
    account_details = APIClient().user.get_user_account()

    yield account_summary, account_details

    logger.info("- Show all account summary items")
    web.home_page.check_uncheck_balance_items(AccSummary.checkbox_list())



