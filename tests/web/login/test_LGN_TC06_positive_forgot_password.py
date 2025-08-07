import pytest

from src.data.enums import AccountType
from src.data.project_info import RuntimeConfig
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_demo, pytest.mark.not_crm]


def test(web, ):
    account_id = 188183338 if RuntimeConfig.account == AccountType.LIVE else None

    logger.info(f"Step 1: Select account tab: {RuntimeConfig.account}")
    web.login_page.select_account_type(RuntimeConfig.account)

    logger.info("Step 2: Click on Forgot Password")
    web.login_page.forgot_password(email="test@test.com", account_id=account_id)

    logger.info("Verify message HELP ON THE WAY")
    web.login_page.verify_text_content(UIMessages.HELP_ON_THE_WAY, UIMessages.FORGOT_PASSWORD_DES)
