from src.data.objects.account_obj import ObjDemoAccount
from src.utils.logging_utils import logger


def test(android):
    account_info = ObjDemoAccount().full_params()

    logger.info("Step 1: Click on open demo account")
    android.home_screen.settings.open_demo_account(account_info)

    logger.info("Verify demo account ready message")
    android.home_screen.settings.demo_account_modal.verify_ready_message()

    logger.info("Verify demo account username is correct")
    android.home_screen.settings.demo_account_modal.verify_account_info(account_info.name)
    # save userid and password for validation
    user_id, password, *_ = android.home_screen.settings.demo_account_modal.get_account_details().values()

    logger.info("Step 4: Click Switch to Demo Account on demo account creation form")
    android.home_screen.settings.demo_account_modal.switch_to_demo_account()

    logger.info("Verify autofill values of account ID and password is correct")
    android.login_screen.verify_account_autofill_value(user_id, password)

    logger.info("Step 5: Click Sign in button")
    android.login_screen.click_sign_in()

    logger.info("Verify login successfully")
    android.home_screen.feature_anm_modal.got_it()
    android.home_screen.verify_account_info_displayed()
