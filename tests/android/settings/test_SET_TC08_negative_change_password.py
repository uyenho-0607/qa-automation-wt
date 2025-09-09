import pytest

from src.core.config_manager import Config
from src.data.ui_messages import UIMessages
from src.utils import random_utils
from src.utils.logging_utils import logger


@pytest.mark.parametrize("password", random_utils.random_invalid_password())
def test(android, password):
    credentials = Config.credentials()

    logger.info(f"Step: Change password to {password!r}")
    android.home_screen.settings.change_password(credentials.password, password)

    logger.info("Verify invalid password alert error")
    android.home_screen.verify_alert_error_message(UIMessages.PASSWORD_INVALID_FORMAT)