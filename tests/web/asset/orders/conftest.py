import pytest

from src.apis.api_client import APIClient
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.fixture(autouse=True)
def disable_OCT(disable_OCT):
    pass


@pytest.fixture(scope="package", autouse=True)
def get_symbol_details(symbol):
    logger.debug(f"- Getting details of symbol {symbol!r}")
    market_details = APIClient().market.get_symbol_details(symbol)

    ObjectTrade.POINT_STEP = market_details.get("pointStep")
    ObjectTrade.DECIMAL = market_details.get("decimal")
    ObjectTrade.CONTRACT_SIZE = market_details.get("contractSize")
    ObjectTrade.STOP_LEVEL = market_details.get("stopsLevel")
