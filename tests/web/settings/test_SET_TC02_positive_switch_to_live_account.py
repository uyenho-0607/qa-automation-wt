import pytest

from src.data.enums import AccountType, SettingOptions
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_live]


@pytest.mark.skip
def test(web):
    logger.info("Step: Switch to live account")
    web.home_page.settings.switch_to_account(SettingOptions.SWITCH_TO_LIVE)

    logger.info("Verify live account tab is selected in Login Page")
    web.login_page.verify_account_tab_is_selected(AccountType.LIVE)
