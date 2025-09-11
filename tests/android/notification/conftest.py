import pytest

from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(android, login_wt_app, symbol, disable_OCT):
    logger.info(f"- Select symbol: {symbol!r}")
    android.home_screen.watch_list.select_tab(WatchListTab.CRYPTO)
    android.home_screen.watch_list.select_symbol(symbol)
