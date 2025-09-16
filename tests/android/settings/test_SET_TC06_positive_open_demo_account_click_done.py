from src.data.objects.account_obj import ObjDemoAccount
from src.utils.logging_utils import logger


def test(android):
    account_info = ObjDemoAccount().full_params()

    logger.info("Step 1: Click on open demo account")
    android.home_screen.settings.open_demo_account(account_info)

    logger.info("Verify demo account ready message")
    android.home_screen.settings.demo_account_modal.verify_ready_message()

    logger.info("Verify setting options is displayed")
    android.home_screen.settings.demo_account_modal.demo_creation_done()
