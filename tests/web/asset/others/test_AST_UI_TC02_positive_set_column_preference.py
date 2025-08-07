import pytest

from src.data.enums import Features, ColPreference
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger


def test(web, pre_setup_order, setup_teardown):
    tab = pre_setup_order
    options = ColPreference.get_random_columns(tab, amount=3)

    logger.info("Step 1: Set Show all columns")
    web.trade_page.asset_tab.set_column_preference(tab, ColPreference.SHOW_ALL, unchecked=False)

    logger.info(f"Step 2: Uncheck {options}")
    web.trade_page.asset_tab.set_column_preference(tab, options, close_modal=True, unchecked=True)

    logger.info("Verify message saved success")
    web.home_page.notifications.verify_alert_success_message(UIMessages.ALL_CHANGES_SAVED)

    logger.info("Verify displayed & not displayed headers")
    web.trade_page.asset_tab.verify_table_headers_displayed(tab, headers=options, is_display=False)

    logger.info("Step 3: Navigate to Trade page")
    web.home_page.navigate_to(Features.TRADE)

    logger.info("Verify headers displayed & not displayed")
    web.assets_page.asset_tab.verify_table_headers_displayed(tab, headers=options, is_display=False)


@pytest.fixture(autouse=True)
def setup_teardown(web, pre_setup_order):
    web.home_page.navigate_to(Features.ASSETS)

    yield
    web.assets_page.asset_tab.set_column_preference(pre_setup_order, ColPreference.SHOW_ALL, unchecked=False)
