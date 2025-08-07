import pytest
from src.utils.logging_utils import logger
from src.utils.random_utils import random_password, random_userid


@pytest.mark.critical
def test(web_app):
    logger.info("Step 1: Login with valid userid and invalid password")
    web_app.login_page.login(password=random_password())

    logger.info(f"Verify login error message is displayed")
    web_app.login_page.verify_alert_error_message()

    logger.info("Step 2: Login with invalid userid and valid password")
    web_app.login_page.login(userid=random_userid())

    logger.info(f"Verify login error message is displayed")
    web_app.login_page.verify_alert_error_message()

    logger.info("Step 3: Login with both invalid userid and password")
    web_app.login_page.login(random_userid(), random_password())

    logger.info(f"Verify login error message is displayed")
    web_app.login_page.verify_alert_error_message()
