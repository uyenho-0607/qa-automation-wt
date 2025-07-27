import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (None, None),
        (SLTPType.random_values(), None),
        (None, SLTPType.random_values()),
        SLTPType.sample_values(amount=2)
    ]
)
def test(web_app, symbol, get_asset_tab_amount, sl_type, tp_type):
    trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol)

    logger.info("Step 1: Get Pending Order tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} order for {symbol!r} (SL:{sl_type}, TP:{tp_type}, tab:{tab_amount})")
    web_app.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    web_app.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm place order")
    web_app.trade_page.modals.confirm_trade()

    logger.info(f"Verify order submitted notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Pending Order tab amount increased to {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Step 4: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order details in Pending Order tab")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)


@pytest.fixture(autouse=True)
def teardown_test(web_app):
    yield
    logger.info("- Teardown test")
    web_app.trade_page.place_order_panel.click_cancel_btn()
