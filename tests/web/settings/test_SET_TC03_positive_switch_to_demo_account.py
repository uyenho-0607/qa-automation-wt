import pytest

from src.data.enums import AccountType, SettingOptions
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_demo]


def test(web):
    logger.info("Step: Switch to demo account")
    web.home_page.settings.switch_to_account(SettingOptions.SWITCH_TO_DEMO)

    logger.info("Verify demo account tab is selected in Login Page")
    web.login_page.verify_account_tab_is_selected(AccountType.DEMO)
