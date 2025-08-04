import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (None, None),
        (SLTPType.random_values(), None),
        (None, SLTPType.random_values()),
        SLTPType.random_values(amount=2)
    ]
)
def test(web, limit_obj, get_asset_tab_amount, sl_type, tp_type, close_confirm_modal):
    trade_object = limit_obj()
    tab = AssetTabs.PENDING_ORDER
    # -------------------

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} order with sl_type: {sl_type!r}, tp_type: {tp_type!r} (tab:{tab_amount!r})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Get current server/ device time")
    web.home_page.get_server_device_time(trade_object)

    logger.info("Step 4: Confirm place order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Step 5: Select tab: {tab.value.title()!r}")
    web.trade_page.asset_tab.select_tab(tab)

    logger.info(f"Verify {tab.value.title()} item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
