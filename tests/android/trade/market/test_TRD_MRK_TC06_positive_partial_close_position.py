import copy

import pytest

from src.data.enums import TradeType, AssetTabs, OrderType, Features
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils import DotDict
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "trade_type", [
        TradeType.BUY,
        TradeType.SELL,
    ]
)
def test(android, symbol, get_asset_tab_amount, trade_type, create_order_data):
    # -------------------
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(AssetTabs.OPEN_POSITION)
    # -------------------
    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    # Object for new created open position
    new_object = DotDict(copy.deepcopy(dict(trade_object)))

    logger.info("Step 3: Partial close position")
    android.trade_screen.asset_tab.partial_close_position(trade_object.order_id, new_object, confirm=True)

    # update new volume, units after partial close
    trade_object.volume, trade_object.units = new_object.close_volume, new_object.close_units

    logger.info("Verify Close Order notification banner")
    exp_noti = ObjectNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Verify asset tab amount = {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Verify Open Position details in asset tab")
    android.trade_screen.asset_tab.verify_item_data(new_object)

    logger.info("Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Verify Position Closed noti in notification box")
    android.trade_screen.navigate_to(Features.HOME)
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())
