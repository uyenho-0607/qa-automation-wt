import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, NotificationTab
from src.data.objects.symbol_obj import ObjSymbol
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def symbol():
    logger.info(f"{'=' * 10} Setup Symbol Data - Start {'=' * 10}")
    logger.info("- Get and select symbol to use through test package", setup=True)
    logger.debug(f"- Filtered symbol list: {(symbols := ObjSymbol().get_symbols())}")
    logger.debug(f"- Random selected symbol: {(select_symbol := random.choice(symbols))!r}")

    logger.info(f"{'=' * 10} Setup Symbol Data - Done {'=' * 10}")
    return select_symbol


@pytest.fixture(scope="package")
def get_asset_tab_amount(symbol):
    def _handler(order_type: OrderType | str):
        res = APIClient().order.get_counts(symbol, order_type)
        logger.debug(f"- Current amount of {order_type.upper()!r}: {res!r}")
        return res

    return _handler


@pytest.fixture(scope="package")
def get_notification_tab_amount():
    def _handler(notification_type: NotificationTab = NotificationTab.ORDER):
        res = APIClient().notification.get_notification_counts(notification_type)
        logger.debug(f"- Current amount of {notification_type.upper()!r}: {res!r}")
        return res

    return _handler
