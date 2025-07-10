from src.data.enums import Language
from src.utils.common_utils import translate_sign_in
from src.utils.logging_utils import logger


def test(web):
    list_value = Language.sample_values(amount=3)

    logger.info(f"Step 1: Change langauge -> {(value := list_value[0])}")
    web.login_page.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    web.login_page.verify_language(value)

    logger.info(f"Step 2: Change langauge -> {(value := list_value[1])}")
    web.login_page.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    web.login_page.verify_language(value)

    logger.info(f"Step 3: Change langauge -> {(value := list_value[-1])}")
    web.login_page.select_language(value)

    logger.info(f"Verify 'Sign in' button is changed to {translate_sign_in(value)!r}")
    web.login_page.verify_language(value)

    logger.info("Step 4: Continue to login ")
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()

    logger.info("Verify login success")
    web.home_page.verify_acc_info_displayed()
