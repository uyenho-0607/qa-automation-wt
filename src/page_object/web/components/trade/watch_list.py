import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import EXPLICIT_WAIT, SHORT_WAIT
from src.data.enums import WatchListTab, Features, URLPaths
from src.data.ui_messages import UIMessages
from src.page_object.web.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element
from src.utils.logging_utils import logger


class WatchList(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #

    # watch list items
    __all_tabs = (By.XPATH, "//div[@data-testid='watchlist-tabs']/div")
    __tab = (By.CSS_SELECTOR, data_testid('tab-{}'))
    __watchlist_container = (By.XPATH, "//div[@data-testid='watchlist-list']/div")
    __item_by_name = (By.XPATH, "//div[@data-testid='watchlist-symbol' and text()='{}']")
    __items = (By.CSS_SELECTOR, data_testid('watchlist-symbol'))
    __selected_item = (
        By.XPATH,
        "//div[contains(@class, 'selected')]//div[@data-testid='watchlist-symbol' and text()='{}']"
    )
    __unstar_icon_by_symbol = (
        By.XPATH,
        "//div[text()='{}']/ancestor::div[@data-testid='watchlist-list-item']"
        "//div[@data-testid='watchlist-star-unwatch']"
    )
    __star_icon_by_symbol = (
        By.XPATH,
        "//div[text()='{}']/ancestor::div[@data-testid='watchlist-list-item']"
        "//div[@data-testid='watchlist-star-watch']"
    )
    __unstarred_icons = (By.CSS_SELECTOR, data_testid('watchlist-star-unwatch'))
    __starred_icons = (By.CSS_SELECTOR, data_testid('watchlist-star-watch'))
    __empty_message = (By.CSS_SELECTOR, "div[data-testid='watchlist-list'] > div[data-testid='empty-message']")

    # ------------------------ ACTIONS ------------------------ #

    def __get_tab_locator(self, tab: WatchListTab):
        """Get correct tab locator based on current page (TRADE or MARKET)"""
        page = None
        if self.is_current_page(URLPaths.MARKETS):
            page = Features.MARKETS

        return cook_element(self.__tab, tab.get_tab(page))

    def __is_tab_selected(self, tab: WatchListTab):
        locator = self.__get_tab_locator(tab)
        return "selected" in self.actions.get_attribute(locator, "class")

    def __select_tab_with_retry(self, tab: WatchListTab, wait=True, retry_count=0):
        locator = self.__get_tab_locator(tab)
        max_retries = 3

        if not self.__is_tab_selected(tab):
            logger.info(f"- Select tab: {tab.value!r}")
            self.actions.click(locator)

            if wait:
                self.wait_for_spin_loader(timeout=5)

        # Retry if tab is still not selected and we haven't exceeded max retries
        if not self.__is_tab_selected(tab) and retry_count < max_retries:
            logger.debug(f"- Retry selecting tab: {tab.value!r}")
            self.__select_tab_with_retry(tab, wait, retry_count + 1)


    def select_tab(self, tab: WatchListTab, wait_for_loader=True):
        """Select a tab and retry if needed (handles edge cases like Favourite tab in MARKET)"""
        if tab in WatchListTab.sub_tabs() and not self.actions.is_element_displayed(self.__get_tab_locator(tab), show_log=False):
            self.__select_tab_with_retry(WatchListTab.ALL, wait_for_loader)

        self.__select_tab_with_retry(tab, wait_for_loader)

    def wait_for_tab_selected(self, tab: WatchListTab, timeout: int = EXPLICIT_WAIT):
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

    def get_all_symbols(self, tab: WatchListTab = None, expected_symbols = None):
        """Get all symbols by scrolling through the watchlist container"""
        if tab:
            self.select_tab(tab)

        all_symbols = set()  # Use set to avoid duplicates
        scroll_attempts = 0
        last_count = 0
        max_scroll_attempts: int = int(len(expected_symbols) / 2)
        logger.debug(f"- Max scroll attempts: {max_scroll_attempts!r}")

        while scroll_attempts < max_scroll_attempts:
            # Get current visible symbols
            current_symbols = self.get_current_symbols(tab)

            # Add new symbols to our set
            new_symbols = set(current_symbols) - all_symbols
            all_symbols.update(new_symbols)

            # Check if we've found all expected symbols
            if set(all_symbols) == set(expected_symbols):
                logger.debug(f"Found all expected symbols after {scroll_attempts + 1} scroll attempts. Stopping early.")
                break

            # Check if we're not finding new symbols (end of list)
            if len(all_symbols) == last_count:
                logger.debug("No new symbols found in this scroll attempt")
                if set(all_symbols) == set(expected_symbols):
                    break
            else:
                last_count = len(all_symbols)

            # Scroll down in the container
            try:
                self.actions.scroll_container_down(self.__watchlist_container, scroll_step=0.5)
            except Exception as e:
                logger.warning(f"Error during scroll: {e}")
                break

            scroll_attempts += 1

        result = list(all_symbols)
        logger.debug(f"Finished scrolling. Total symbols collected: {len(result)}")
        return result

    def get_current_symbols(self, tab: WatchListTab = None):
        """Get current displayed symbols on screen"""
        if tab:
            self.select_tab(tab)

        elements = self.actions.find_elements(self.__items)
        if elements:
            res = [ele.text.strip() for ele in elements]
            return [item for item in res if item]
        return []

    def get_random_symbol(self, tab=None):
        cur_symbols = self.get_current_symbols(tab)
        return random.choice(cur_symbols[:5 if len(cur_symbols) > 5 else int(len(cur_symbols)/2)])

    def get_last_symbol(self, tab: WatchListTab | list[WatchListTab], store_data: DotDict = None):
        """Get latest symbol of each input tab (tab can be str or list)"""
        tab_list = tab if isinstance(tab, list) else [tab]
        res = {}
        for tab in tab_list:
            self.select_tab(tab)
            res[tab] = self.actions.get_text(self.__items)

        if store_data is not None:
            store_data |= res
        return res

    def select_symbol(self, symbol, tab=None):
        """Select symbol from current displayed list"""
        # todo: enhance add scrolldown until seeing the symbol
        if tab:
            self.select_tab(tab)
        self.actions.click(cook_element(self.__item_by_name, symbol))

    def select_last_symbol(self, tab: WatchListTab = WatchListTab.ALL):
        self.select_tab(tab)
        self.actions.click(self.__items)

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

        if symbols:
            for symbol in symbols:
                logger.debug(f"Marking star/unstar for symbol: {symbol!r}")
                star_locator = cook_element(symbol_icon_locator, symbol)
                if self.actions.is_element_displayed(star_locator):
                    self.actions.click(star_locator)
                    time.sleep(1)

        elif all_symbols:
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
        """If symbol is empty, mark whether all_symbols (True) or latest symbol (False)"""
        self.__toggle_star_symbol(symbols, all_symbols, mark_star=True)

    def mark_unstar_symbols(self, symbol: str | list = None, all_symbols: bool = False):
        self.__toggle_star_symbol(symbol, all_symbols, mark_star=False)

    # ------------------------ VERIFY ------------------------ #
    def verify_empty_message(self):
        super().verify_empty_message(self.__empty_message, UIMessages.NO_ITEM_AVAILABLE)

    def verify_tabs_displayed(self):
        expected_tabs = WatchListTab.parent_tabs() + [item.name.capitalize() for item in WatchListTab.sub_tabs()]
        actual_tabs = self.actions.find_elements(self.__all_tabs)
        list_values = [ele.text.strip() for ele in actual_tabs]
        soft_assert(list_values, expected_tabs)

    def verify_tab_selected(self, tab: WatchListTab = WatchListTab.ALL):
        soft_assert(self.wait_for_tab_selected(tab), True, error_message=f"Tab {tab.capitalize()} is not selected")

    def verify_symbol_selected(self, symbol: str):
        """Verify selected item"""
        self.actions.verify_element_displayed(cook_element(self.__selected_item, symbol))

    def verify_symbols_starred(self, symbols: str, is_starred: bool = True):
        """Verify symbol star status"""
        symbols = symbols if isinstance(symbols, list) else [symbols]
        locator = self.__star_icon_by_symbol if is_starred else self.__unstar_icon_by_symbol
        locators = [cook_element(locator, symbol) for symbol in symbols]

        self.actions.verify_elements_displayed(locators, timeout=SHORT_WAIT)

    def verify_symbols_displayed(self, tab: WatchListTab = None, symbols: str | list = None, is_display=True):
        """Verify symbol is displayed in tab"""
        if tab:
            self.select_tab(tab)

        symbols = symbols if isinstance(symbols, list) else [symbols]
        locator_list = [cook_element(self.__item_by_name, symbol) for symbol in symbols]
        self.actions.verify_elements_displayed(locator_list, timeout=SHORT_WAIT, is_display=is_display)

    def verify_symbols_list(self, tab=None, symbols=None):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        current_symbols = self.get_all_symbols(tab, expected_symbols=symbols)

        soft_assert(
            sorted(current_symbols) == sorted(symbols), True,
            error_message=f"Missing: {[item for item in symbols if item not in current_symbols]}, Redundant: {[item for item in current_symbols if item not in symbols]}"
        )
