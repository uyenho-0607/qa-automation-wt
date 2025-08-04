import random

from src.data.enums import Language
from src.utils.common_utils import translate_sign_in
from src.utils.logging_utils import logger


def test(web_app):
    list_value = random.sample(Language.list_values(), k=3)

    logger.info(f"Step 1: Change langauge -> {(value := list_value[0])}")
    web_app.login_page.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    web_app.login_page.verify_language(value)

    logger.info(f"Step 2: Change langauge -> {(value := list_value[1])}")
    web_app.login_page.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    web_app.login_page.verify_language(value)

    logger.info(f"Step 3: Change langauge -> {(value := list_value[-1])}")
    web_app.login_page.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    web_app.login_page.verify_language(value)

    logger.info("Step 4: Continue to login ")
    web_app.login_page.login()

    logger.info("Verify login success")
    web_app.home_page.verify_account_info_displayed()
