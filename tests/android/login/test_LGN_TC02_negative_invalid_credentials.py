import pytest

from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger
from src.utils.random_utils import random_password, random_userid


@pytest.mark.critical
def test(android):
    logger.info("Step 1: Login with valid userid and invalid password")
    android.login_screen.login(password=random_password())

    logger.info(f"Verify {UIMessages.LOGIN_INVALID_CREDENTIALS!r} error message is displayed")
    android.login_screen.verify_alert_error_message(UIMessages.LOGIN_INVALID_CREDENTIALS)

    logger.info("Step 2: Login with invalid userid and valid password")
    android.login_screen.login(userid=random_userid())

    logger.info(f"Verify {UIMessages.LOGIN_INVALID_CREDENTIALS!r} error message is displayed")
    android.login_screen.verify_alert_error_message(UIMessages.LOGIN_INVALID_CREDENTIALS)

    logger.info("Step 3: Login with both invalid userid and password")
    android.login_screen.login(random_userid(), random_password())

    logger.info(f"Verify {UIMessages.LOGIN_INVALID_CREDENTIALS!r} error message is displayed")
    android.login_screen.verify_alert_error_message(UIMessages.LOGIN_INVALID_CREDENTIALS)
