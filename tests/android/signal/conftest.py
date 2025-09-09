import pytest

from src.data.enums import SignalTab, Features
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_wt_app, android):
    logger.info("- Navigate to Signal screen")
    android.home_screen.navigate_to(Features.SIGNAL)


@pytest.fixture
def get_current_symbol(android):
    def _handler(tab: SignalTab = SignalTab.SIGNAL_LIST_TAB):
        symbols = android.signal_screen.get_current_symbols(tab)
        return symbols

    return _handler
