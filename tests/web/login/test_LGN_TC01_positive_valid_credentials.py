import pytest

from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web):
    logger.info("Step 1: Login with valid userid and password")
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()

    logger.info("Verify trade/ home page URL is correct")
    web.home_page.verify_page_url()

    logger.info("Verify account info is displayed")
    web.home_page.verify_acc_info_displayed()

    logger.info("Verify Watch List Tabs displayed in correct order")
    web.trade_page.watch_list.verify_tabs_displayed()

    logger.info("Step 2: Logout")
    web.home_page.settings.logout()

    logger.info("Verify login page URL is correct")
    web.login_page.verify_page_url()

    logger.info("Verify login account tabs is displayed")
    web.login_page.verify_account_tabs_is_displayed()
