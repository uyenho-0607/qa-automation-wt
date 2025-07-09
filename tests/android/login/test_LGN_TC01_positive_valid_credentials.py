from src.utils.logging_utils import logger

def test(android, ):
    logger.info("Step 1: Login with valid userid and password")
    android.login_screen.login()

    logger.info("Verify account info is displayed")
    android.home_screen.verify_acc_info_displayed()

    logger.info("Step 2: User tries to logout")
    android.home_screen.settings.logout()

    logger.info("Verify login account tabs is displayed")
    android.login_screen.verify_account_tab_is_displayed()
