import pytest

from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(login_wt_app, symbol, ios):

    logger.info(f"- Search and select symbol: {symbol!r}", setup=True)
    ios.home_screen.search_and_select_symbol(symbol)