import random

import pytest

from src.apis.api_client import APIClient
from src.data.consts import get_symbols
from src.data.enums import OrderType
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def symbol():
    return random.choice(get_symbols())


@pytest.fixture(scope="package")
def get_asset_tab_amount(symbol):
    def _handler(order_type: OrderType | str):
        res = APIClient().order.get_counts(symbol, order_type)
        logger.debug(f"- Current amount of {order_type.upper()!r}: {res!r}")
        return res

    return _handler
