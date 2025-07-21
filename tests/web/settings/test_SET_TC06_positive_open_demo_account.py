import pytest

from src.data.enums import AccountType
from src.data.objects.account_obj import ObjDemoAccount
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_demo, pytest.mark.not_crm]


def test(web):
    account_info = ObjDemoAccount().full_params()

    logger.info("Step 1: Click on open demo account")
    web.home_page.settings.open_demo_account(account_info)

    logger.info("Verify demo account ready message")
    web.home_page.settings.demo_account_modal.verify_ready_message()

    logger.info("Verify demo account username is correct")
    web.home_page.settings.demo_account_modal.verify_account_info(account_info.name)
    # save userid and password for validation
    user_id, password, *_ = web.home_page.settings.demo_account_modal.get_account_details().values()

    logger.info("Step 4: Click Sign in button on demo account creation form")
    web.home_page.settings.demo_account_modal.sign_in_from_completion()

    logger.info("Verify demo tab is being selected")
    web.login_page.verify_account_tab_is_selected(AccountType.DEMO)

    logger.info("Verify autofill values of account ID and password is correct")
    web.login_page.verify_account_autofill_value(user_id, password)

    logger.info("Step 5: Click Sign in button")
    web.login_page.click_sign_in()

    logger.info("Verify login successfully")
    web.home_page.feature_announcement_modal.got_it()
    web.home_page.verify_acc_info_displayed()
