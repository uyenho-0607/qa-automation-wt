import pytest

from src.data.enums import AccountType
from src.data.project_info import ProjectConfig
from src.data.ui_messages import UIMessages

pytestmark = [pytest.mark.not_demo]


def test(web, ):
    account_id = 188183338 if ProjectConfig.account == AccountType.LIVE else None

    web.login_page.select_account_type(ProjectConfig.account)
    web.login_page.forgot_password(email="test@test.com", account_id=account_id)
    web.login_page.verify_text_content(UIMessages.HELP_ON_THE_WAY, UIMessages.FORGOT_PASSWORD_DES)
