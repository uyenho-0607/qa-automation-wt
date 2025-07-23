import random
import time

import pytest
from src.data.enums import AssetTabs, OrderType, TradeType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("trade_type", random.choices([TradeType.BUY, TradeType.SELL], k=1))
def test(web, symbol, get_asset_tab_amount, cancel_close_order, trade_type, create_order_data):

    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_type.value.upper()} {trade_object.order_type.upper()} Order")
    create_order_data(trade_object)

    logger.info(f"Verify order placed successfully - tab_amount increased by 1: {(tab_amount := tab_amount + 1)!r}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    # Object for new created open position
    new_object = ObjTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})

    logger.info(f"Step 2: Partial close position - {trade_object.get('order_id')!r} - tab amount: {tab_amount!r}")
    time.sleep(1)
    web.trade_page.asset_tab.partial_close_position(trade_object=new_object)

    # update new volume, units after partial close
    trade_object.volume, trade_object.units = new_object.close_volume, new_object.close_units

    logger.info("Verify Close order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_object).position_closed_details())

    logger.info(f"Verify asset tab amount remains unchanged for partial closed: {tab_amount!r}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info("Verify Open Position details in asset tab")
    web.trade_page.asset_tab.verify_item_data(new_object)

    logger.info("Verify history order details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
