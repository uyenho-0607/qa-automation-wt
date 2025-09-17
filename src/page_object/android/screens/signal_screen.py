import random
import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import SignalTab, OrderType
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.trading_modals import TradingModals
from src.page_object.android.components.trade.chart import Chart
from src.page_object.android.components.trade.place_order_panel import PlaceOrderPanel
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.format_utils import remove_comma
from src.utils.logging_utils import logger


class SignalScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.chart = Chart(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.trading_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __txt_signal_search = (AppiumBy.XPATH, "//android.widget.TextView/following-sibling::android.widget.EditText")
    __tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{}")')
    __items = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("watchlist-symbol")')
    __item_by_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("watchlist-symbol").text("{}")')

    ##### COPY TO ORDER #####
    __analysis_action = (
        AppiumBy.XPATH,
        "(//android.widget.TextView[@text='Action']/following-sibling::android.widget.TextView)[4]"  # BUY or SELL
    )
    __analysis_order_status = (
        AppiumBy.XPATH,
        "(//android.widget.TextView[@text='Order Status']/following-sibling::android.widget.TextView)[4]"  # Order Type
    )
    __analysis_tp = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text, 'Take Profit')]/following-sibling::android.widget.TextView"
    )
    __analysis_sl = (
        AppiumBy.XPATH, "(//android.widget.TextView[@text='Stop Loss']/following-sibling::android.widget.TextView)[3]"
    )
    __analysis_entry = (
        AppiumBy.XPATH, "(//android.widget.TextView[@text='Entry']/following-sibling::android.widget.TextView)[3]"
    )
    __btn_copy_to_order = (AppiumBy.XPATH, "(//android.widget.TextView[@text='COPY TO ORDER'])[{}]")

    # ------------------------ ACTIONS ------------------------ #

    def search_signal(self, value: str):
        self.actions.send_keys(self.__txt_signal_search, value)

    def select_tab(self, tab: SignalTab):
        self.actions.click(cook_element(self.__tab, tab))

    def get_current_symbols(self, tab: SignalTab = SignalTab.SIGNAL_LIST_TAB):
        """Get current displayed symbols on screen"""
        self.select_tab(tab)
        symbols = self.actions.get_text_elements(self.__items)
        logger.debug(f"- Current symbols: {', '.join(symbols)}")
        return symbols

    def place_order_with_copy_trade(self, signal="", trade_object: DotDict = None, confirm=True):
        self.wait_for_spin_loader()
        self.actions.click(cook_element(self.__item_by_name, signal))

        # randomly choose take profit
        tp_index = random.randint(1, 2)
        time.sleep(0.5)

        self.actions.scroll_down()

        self.actions.click(cook_element(self.__btn_copy_to_order, tp_index))

        take_profit = self.actions.find_elements(self.__analysis_tp)
        if trade_object is not None:

            trade_object |= {
                "trade_type": self.actions.get_text(self.__analysis_action).upper(),
                "order_type": OrderType(self.actions.get_text(self.__analysis_order_status).split(" ")[-1].lower()),
                "take_profit": remove_comma(take_profit[tp_index - 1].text.strip()),
                "stop_loss": remove_comma(self.actions.get_text(self.__analysis_sl)),
            }

            # Update entry price if Order Type != Market
            trade_object.entry_price = self.place_order_panel.get_live_price(trade_object.trade_type)
            if trade_object.order_type != OrderType.MARKET:
                trade_object.entry_price = remove_comma(self.actions.get_text(self.__analysis_entry))

        # input volume
        volume = random.randint(1, 10)
        self.place_order_panel._input_volume(volume)

        trade_object.volume = volume
        trade_object.units = self.place_order_panel._get_volume_info_value()
        self.place_order_panel._click_place_order_btn()
        not confirm or self.place_order_panel.confirm_trade()

    # ------------------------ VERIFY ------------------------ #

    def verify_search_result(self, search_key: str, check_contains=False):
        signals = self.get_current_symbols()
        for item in signals:
            soft_assert(item, search_key, check_contains=check_contains)
