import pytest

from src.data.enums import AssetTabs, SLTPType, Features
from src.data.objects.notification_obj import ObjNoti
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
def test(web_app, cancel_all, sl_type, tp_type, market_obj):
    trade_object = market_obj()
    tab = AssetTabs.OPEN_POSITION

    logger.info("Step 1: Get asset tab amount")
    tab_amount = web_app.trade_page.asset_tab.get_tab_amount(tab)

    logger.info(f"Step 2: Place {trade_object.trade_type} order for {trade_object.symbol!r} (SL:{sl_type}, TP:{tp_type}, tab:{tab_amount})")
    web_app.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    web_app.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm place order")
    web_app.trade_page.modals.confirm_trade()

    logger.info(f"Verify order submitted notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify order details in tab")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Step 3: Navigate to Home Screen")
    web_app.trade_page.navigate_to(Features.HOME)

    logger.info("Verify Open Position Notification")
    web_app.home_page.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(order_id=trade_object.order_id), close=True)


@pytest.fixture(autouse=True)
def teardown_test(web_app):
    yield
    logger.info("- Navigate back to Trade Screen")
    web_app.home_page.navigate_to(Features.TRADE)