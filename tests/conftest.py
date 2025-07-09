import operator
import random

import pytest
from src.apis.api_client import APIClient
from src.data.consts import SYMBOLS
from src.data.enums import OrderType, BulkCloseOpts
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.utils.format_utils import format_prices
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def symbol():
    selected_symbol = random.choice(SYMBOLS[ProjectConfig.server])

    logger.debug(f"- Getting details of symbol {selected_symbol!r}")
    market_details = APIClient().market.get_symbol_details(selected_symbol)

    ObjectTrade.POINT_STEP = market_details.get("pointStep")
    ObjectTrade.DECIMAL = market_details.get("decimal")
    ObjectTrade.CONTRACT_SIZE = market_details.get("contractSize")

    return selected_symbol

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


@pytest.fixture
def update_entry_price(web):
    def _handler(trade_object):

        logger.debug("- Get last order_id")
        web.trade_page.asset_tab.get_last_order_id(trade_object)

        if trade_object.order_type == OrderType.MARKET:
            resp = APIClient().order.get_orders_details(
                symbol=trade_object.symbol, order_id=trade_object.order_id
            )

            if resp.get("openPrice"):
                logger.debug(f"- Update entry price from {trade_object.entry_price} to {resp["openPrice"]}")
                trade_object["entry_price"] = format_prices(round(resp["openPrice"], ndigits=ObjectTrade.DECIMAL), ObjectTrade.DECIMAL)

        return None

    return _handler
