import random

from src.data.enums import Language
from src.utils.common_utils import translate_sign_in
from src.utils.logging_utils import logger


def test(android):
    list_value = random.sample(Language.list_values(), k=3)

    logger.info(f"Step 1: Change langauge -> {(value := list_value[0])}")
    android.login_screen.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    android.login_screen.verify_language(value)

    logger.info(f"Step 2: Change langauge -> {(value := list_value[1])}")
    android.login_screen.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    android.login_screen.verify_language(value)

    logger.info(f"Step 3: Change langauge -> {(value := list_value[-1])}")
    android.login_screen.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    android.login_screen.verify_language(value)

    logger.info("Step 4: Continue to login ")
    android.login_screen.login()

    logger.info("Verify login success")
    android.home_screen.verify_account_info_displayed()