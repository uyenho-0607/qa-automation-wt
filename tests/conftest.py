import operator
import random

import pytest

from src.apis.api_client import APIClient
from src.data.consts import get_symbols
from src.data.enums import OrderType, BulkCloseOpts
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def symbol():
    return random.choice(get_symbols())


@pytest.fixture
def get_order_id_list(symbol):
    def _handler(order_type: OrderType = OrderType.MARKET, close_option=BulkCloseOpts.ALL):
        resp = APIClient().order.get_order_id_list(symbol, order_type)

        if close_option == BulkCloseOpts.ALL:
            return [item["orderId"] for item in resp]

        cond = operator.ge if close_option == BulkCloseOpts.PROFIT else operator.le
        return [item["orderId"] for item in resp if cond(item["profit"], 0)]

    return _handler


@pytest.fixture(scope="package")
def get_asset_tab_amount(symbol):
    def _handler(order_type: OrderType | str):
        res = APIClient().order.get_counts(symbol, order_type)
        logger.debug(f"- Current amount of {order_type.upper()!r}: {res!r}")
        return res

    return _handler
