import pytest

from src.utils.logging_utils import logger
from src.utils.random_utils import random_password, random_userid


@pytest.mark.critical
def test(web):

    logger.info("Step 1: Login with VALID userid and INVALID password")
    web.login_page.login(password=random_password(), wait=False)

    logger.info(f"Verify Invalid Login error message is displayed")
    web.login_page.verify_alert_error_message()

    logger.info("Verify URL remains on login page")
    web.login_page.verify_page_url()

    logger.info("Step 2: Login with INVALID userid and VALID password")
    web.login_page.login(random_userid(), wait=False)

    logger.info(f"Verify Invalid Login error message is displayed")
    web.login_page.verify_alert_error_message()

    logger.info("Verify URL remains on login page")
    web.login_page.verify_page_url()

    logger.info("Step 3: Login with BOTH INVALID userid and password")
    web.login_page.login(random_userid(), random_password(), wait=False)

    logger.info(f"Verify Invalid Login error message is displayed")
    web.login_page.verify_alert_error_message()

    logger.info("Verify URL remains on login page")
    web.login_page.verify_page_url()
