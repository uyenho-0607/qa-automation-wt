import pytest

from src.apis.api_client import APIClient
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(android, get_current_symbol):
    selected_symbol = get_current_symbol()[0]
    trade_object = ObjTrade(symbol=selected_symbol)

    logger.info("Step 1: Place order with copy trade")
    android.signal_screen.place_order_with_copy_trade(selected_symbol, trade_object, confirm=False)

    logger.info("Verify order submitted notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())


@pytest.fixture(autouse=True)
def setup_test(enable_OCT):
    yield
    logger.info("- Enable OCT")
    APIClient().user.patch_oct(enable=False)
