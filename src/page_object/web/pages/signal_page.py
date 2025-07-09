import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import EXPLICIT_WAIT
from src.data.enums import URLPaths, SignalTab, OrderType
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.modals.trading_modals import TradingModals
from src.page_object.web.components.trade.chart import Chart
from src.page_object.web.components.trade.place_order_panel import PlaceOrderPanel
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.format_utils import remove_commas
from src.utils.logging_utils import logger


class SignalPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.chart = Chart(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.trading_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __txt_signal_search = (By.CSS_SELECTOR, "input[placeholder='Search signals']")
    __tab = (By.CSS_SELECTOR, data_testid('signal-filter-{}'))
    __items = (By.CSS_SELECTOR, data_testid('signal-row-symbol'))
    __item_by_name = (By.XPATH, "//div[@data-testid='signal-row-symbol' and text()='{}']")
    __selected_item = (
        By.XPATH,
        "//tr[@data-testid='signal-row' and contains(@class, 'selected')]//div[@data-testid='signal-row-symbol']"
    )

    __unstar_icon_by_symbol = (
        By.XPATH,
        "//div[text()='{}']/ancestor::*[@data-testid='signal-row']"
        "//div[@data-testid='signal-row-star-unwatch']"
    )
    __star_icon_by_symbol = (
        By.XPATH,
        "//div[text()='{}']/ancestor::*[@data-testid='signal-row']"
        "//div[@data-testid='signal-row-star-watch']"
    )

    __unstarred_icons = (By.CSS_SELECTOR, data_testid('signal-row-star-unwatch'))
    __starred_icons = (By.CSS_SELECTOR, data_testid('signal-row-star-watch'))

    ##### COPY TO ORDER #####
    __analysis_action = (
        By.XPATH,
        "//div[@data-testid='analysis-description-title' and text()='Action']"
        "/parent::div//span[@data-testid='analysis-description-value']"  # BUY or SELL
    )
    __analysis_order_status = (
        By.XPATH,
        "//div[@data-testid='analysis-description-title' and text()='Order Status']"
        "/parent::div//span[@data-testid='analysis-description-value']"  # Order Type
    )

    __analysis_tp = (
        By.XPATH,
        "//div[@data-testid='analysis-action-title' and contains(normalize-space(text()), 'Take Profit')]"
        "/following-sibling::div[@data-testid='analysis-action-value']"
    )
    __analysis_sl = (
        By.XPATH,
        "//div[@data-testid='analysis-action-title' and contains(normalize-space(text()), 'Stop Loss')]"
        "/following-sibling::div[@data-testid='analysis-action-value']"
    )
    __analysis_entry = (
        By.XPATH,
        "//div[@data-testid='analysis-action-title' and contains(normalize-space(text()), 'Entry')]"
        "/following-sibling::div[@data-testid='analysis-action-value']"
    )
    __btn_copy_to_order = (By.CSS_SELECTOR, data_testid('copy-to-order-{}'))

    # ------------------------ ACTIONS ------------------------ #
    def verify_page_url(self):
        super().verify_page_url(URLPaths.SIGNAL)

    def clear_search_field(self):
        self.actions.clear_field(self.__txt_signal_search)

    def search_signal(self, value: str):
        self.clear_search_field()
        self.actions.send_keys(self.__txt_signal_search, value)

    def select_tab(self, tab: SignalTab):
        self.actions.click(cook_element(self.__tab, tab.lower()))
        self.wait_for_spin_loader()

    def get_current_symbols(self, tab: SignalTab = SignalTab.SIGNAL_LIST):
        """Get current displayed symbols on screen"""
        self.select_tab(tab)
        elements = self.actions.find_elements(self.__items)
        if elements:
            return [ele.text.strip() for ele in elements]
        return []

    def __toggle_star_symbol(self, symbols: str | list = None, all_symbols: bool = False, mark_star: bool = True):
        """Helper function to toggle star status for symbols
        Args:
            symbols: Specific symbol to toggle star status. If empty, will toggle based on all_symbols parameter
            all_symbols: If True, toggles all applicable symbols. If False, toggles only the most recent symbol
            mark_star: If True, marks with star. If False, removes star
        """
        icon_locator = self.__unstarred_icons if mark_star else self.__starred_icons
        symbol_icon_locator = self.__unstar_icon_by_symbol if mark_star else self.__star_icon_by_symbol
        symbols = symbols if isinstance(symbols, list) else [symbols] if symbols else []

        for symbol in symbols:
            logger.debug(f"Marking star/unstar for symbol: {symbol!r}")
            star_locator = cook_element(symbol_icon_locator, symbol)
            if self.actions.is_element_displayed(star_locator):
                self.actions.click(star_locator)
                time.sleep(0.5)

        if all_symbols:
            logger.debug("Marking star/unstar for all current symbols")
            max_attempts = 50  # Prevent infinite loop
            for _ in range(max_attempts):
                if not self.actions.is_element_displayed(icon_locator):
                    break
                self.actions.click(icon_locator)
        else:
            logger.debug("Marking star/unstar most recent symbol")
            if self.actions.is_element_displayed(icon_locator):
                self.actions.click(icon_locator)

    def mark_star_symbols(self, symbols: str | list = None, all_symbols: bool = False):
        """Mark symbols with star"""
        self.__toggle_star_symbol(symbols, all_symbols, mark_star=True)

    def mark_unstar_symbols(self, symbol: str | list = None, all_symbols: bool = False):
        """Remove star from symbols"""
        self.__toggle_star_symbol(symbol, all_symbols, mark_star=False)

    def __is_tab_selected(self, tab: SignalTab):
        locator = cook_element(self.__tab, tab.lower())
        return "selected" in self.actions.get_attribute(locator, "class")

    def wait_for_tab_selected(self, tab: SignalTab, timeout: int = EXPLICIT_WAIT):
        """Wait for a specific tab to become selected
        Returns: bool: True if the tab becomes selected within the timeout, False otherwise
        """
        logger.debug(f"Wait for tab {tab.name} to be selected")
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.__is_tab_selected(tab):
                return True
            time.sleep(0.5)
        return False

    def place_order_with_copy_trade(self, signal="", trade_object: DotDict = None, confirm=True):
        self.wait_for_spin_loader()
        self.actions.click(cook_element(self.__item_by_name, signal))

        # randomly choose take profit
        tp_index = random.randint(1, 2)
        time.sleep(0.5)
        self.actions.click(cook_element(self.__btn_copy_to_order, tp_index))

        take_profit = self.actions.find_elements(self.__analysis_tp)
        if trade_object is not None:

            trade_object |= {
                "trade_type": self.actions.get_text(self.__analysis_action).upper(),
                "order_type": self.actions.get_text(self.__analysis_order_status).split(" ")[-1],
                "take_profit": remove_commas(take_profit[tp_index - 1].text.strip()),
                "stop_loss": remove_commas(self.actions.get_text(self.__analysis_sl)),
            }

            # Update entry price if Order Type != Market
            trade_object.entry_price = self.place_order_panel.get_live_price(trade_object.trade_type)
            if trade_object.order_type != OrderType.MARKET:
                trade_object.entry_price = remove_commas(self.actions.get_text(self.__analysis_entry))

        # input volume
        volume = random.randint(1, 10)
        self.place_order_panel._input_volume(volume)

        trade_object.volume = volume
        trade_object.units = self.place_order_panel._get_volume_info_value()
        self.place_order_panel._click_place_order_btn()
        not confirm or self.place_order_panel.confirm_trade()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_is_selected(self, tab: SignalTab):
        soft_assert(self.wait_for_tab_selected(tab), True, error_message=f"Tab {tab.capitalize()} is not selected")

    def verify_symbol_starred(self, symbol: str, is_starred: bool = True):
        """Verify symbol star status"""
        locator = self.__star_icon_by_symbol if is_starred else self.__unstar_icon_by_symbol
        self.actions.verify_element_displayed(cook_element(locator, symbol))

    def verify_symbols_displayed_in_tab(self, tab: SignalTab, symbols: str | list = None, is_display=True):
        """Verify symbol is displayed in tab"""
        self.select_tab(tab)
        symbols = symbols if isinstance(symbols, list) else [symbols]
        for symbol in symbols:
            self.actions.verify_element_displayed(
                cook_element(self.__item_by_name, symbol), is_display=is_display
            )

    def verify_search_result(self, search_key: str, check_contains=False):
        signals = self.get_current_symbols()
        for item in signals:
            soft_assert(item, search_key, check_contains=check_contains)

    def verify_signal_selected(self, symbol):
        selected_symbol = self.actions.get_text(self.__selected_item)
        soft_assert(selected_symbol, symbol)
