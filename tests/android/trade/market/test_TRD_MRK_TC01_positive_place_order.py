import pytest

from src.data.enums import AssetTabs, OrderType, Features, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type", (
            [None, None],
            [SLTPType.PRICE, SLTPType.PRICE],
            [SLTPType.POINTS, SLTPType.POINTS],
            SLTPType.sample_values(amount=2),
    )
)
def test(android, symbol, get_asset_tab_amount, sl_type, tp_type, ):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab = AssetTabs.OPEN_POSITION
    # -------------------

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} order for {symbol!r} (SL:{sl_type}, TP:{tp_type}, tab:{tab_amount})")
    android.trade_screen.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    android.trade_screen.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm place order")
    android.trade_screen.modals.confirm_trade()

    logger.info(f"Verify order submitted notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info("Step 4: Get placed order_id")
    android.trade_screen.asset_tab.get_last_order_id(trade_object)

    logger.info("Step 5: Navigate to Home Screen")
    android.home_screen.navigate_to(Features.HOME)

    logger.info(f"Verify Open Position noti in Notification Box")
    android.home_screen.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id))

    logger.info("Step 6: Navigate to Trade Screen")
    android.home_screen.navigate_to(Features.TRADE)

    logger.info(f"Verify {tab.title()} tab amount increased to {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify order details in {tab.title()} tab")
    android.trade_screen.asset_tab.verify_item_data(trade_object)


@pytest.fixture(autouse=True)
def teardown_test(android):
    yield
    logger.info("- Teardown test")
    android.trade_screen.place_order_panel.click_cancel_btn()
