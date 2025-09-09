import pytest

from src.data.enums import NotiSettingsOpts
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_demo]


def test_new_login_toggle_on(android):
    logger.info("Step 1: Enable new login in notification setting")
    android.home_screen.settings.toggle_noti_settings(NotiSettingsOpts.NEW_LOGINS)

    logger.info("Step 2: Log out & re-login")
    android.home_screen.settings.logout()
    android.login_screen.login()

    logger.info("Verify New Login system notification")
    android.home_screen.notifications.verify_notification_result(
        [UIMessages.NEW_LOGIN_DETECTED, UIMessages.REVIEW_LINKED_DEVICE, "a few seconds ago"], is_system=True
    )

    android.home_screen.go_back()


def test_new_login_toggle_off(android):
    logger.info("Step 1: Disable new login in notification setting")
    android.home_screen.settings.toggle_noti_settings(NotiSettingsOpts.NEW_LOGINS)

    logger.info("Step 2: Log out & re-login")
    android.home_screen.settings.logout()
    android.login_screen.login()
