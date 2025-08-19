import random

from src.data.enums import Language
from src.utils.common_utils import translate_sign_in
from src.utils.logging_utils import logger


def test(ios):
    list_value = random.sample(Language.list_values(), k=3)

    logger.info(f"Step 1: Change langauge -> {(value := list_value[0])}")
    ios.login_screen.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    ios.login_screen.verify_language(value)

    logger.info(f"Step 2: Change langauge -> {(value := list_value[1])}")
    ios.login_screen.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    ios.login_screen.verify_language(value)

    logger.info(f"Step 3: Change langauge -> {(value := list_value[-1])}")
    ios.login_screen.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    ios.login_screen.verify_language(value)

    logger.info("Step 4: Continue to login ")
    ios.login_screen.login()

    logger.info("Verify login success")
    ios.home_screen.verify_account_info_displayed()