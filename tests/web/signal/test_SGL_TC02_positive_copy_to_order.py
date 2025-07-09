import random

from src.data.consts import SYMBOLS
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.utils.logging_utils import logger


def test(web, get_current_symbol):
    selected_symbol = get_current_symbol()[0]
    trade_object = ObjectTrade(symbol=selected_symbol)

    logger.info("Step 1: Place order with copy trade")
    web.signal_page.place_order_with_copy_trade(selected_symbol, trade_object)

    logger.info("Verify order submitted notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())
