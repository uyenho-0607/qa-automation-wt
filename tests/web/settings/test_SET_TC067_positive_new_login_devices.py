import pytest

from src.data.enums import NotiSettingsOpts
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_demo]

def test(web, ):
    logger.info("Step 1: Enable new login in notification setting")
    web.home_page.settings.toggle_noti_settings(NotiSettingsOpts.NEW_LOGINS)

    logger.info("Step 2: Log out & re-login")
    web.home_page.settings.logout()
    web.login_page.login()

    logger.info("Verify New Login system notification")
    web.home_page.notifications.verify_notification_result(
        [UIMessages.NEW_LOGIN_DETECTED, UIMessages.REVIEW_LINKED_DEVICE, "a few seconds ago"], is_system=True
    )
