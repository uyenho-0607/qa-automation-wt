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

    def __select_tab_with_retry(self, tab: WatchListTab, wait=True, retry_count=0, max_retries=3):
        """Recursively try to select the tab."""
        # stop condition
        if self.__is_tab_selected(tab):
            return

        if retry_count >= max_retries:
            logger.warning("- Failed to select tab")

        logger.info(f"- Select tab: {tab.value.title()!r}")
        self.actions.click(self.__get_tab_locator(tab))
        not wait or self.wait_for_spin_loader(timeout=3)

        if self.__is_tab_selected(tab):
            logger.debug(f"- Tab {tab.value.title()} is selected")
            return

        self.__select_tab_with_retry(tab, wait, retry_count + 1)


    def select_tab(self, tab: WatchListTab, wait=True):
        """Select a tab and retry if needed (handles edge cases like Favourite tab in MARKET)"""
        if tab in WatchListTab.sub_tabs() and not self.actions.is_element_displayed(self.__get_tab_locator(tab), show_log=False):
            self.__select_tab_with_retry(WatchListTab.ALL, wait)

        self.__select_tab_with_retry(tab, wait)

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

    def _scroll_watchlist_container(self, scroll_step=0.7):
        self.actions.scroll_container_down(self.__watchlist_container, scroll_step=scroll_step)


    def get_all_symbols(self, tab: WatchListTab = None, expected_symbols = None):
        """Get all symbols by scrolling through the watchlist container"""
        if tab:
            self.select_tab(tab)

        all_symbols = set()  # Use set to avoid duplicates
        scroll_attempts = 0
        last_count = 0
        not_found_time = 0
        max_scroll_attempts = int(len(expected_symbols) / 2) if len(expected_symbols) > 10 else 100
        logger.debug(f"- Max scroll attempts: {max_scroll_attempts!r}")

        while scroll_attempts < max_scroll_attempts:
            # Get current visible symbols
            current_symbols = self.get_current_symbols(tab)

            # Add new symbols to our set
            new_symbols = set(current_symbols) - all_symbols
            all_symbols.update(new_symbols)

            # Check if we've found all expected symbols
            if all(item in all_symbols for item in expected_symbols):
                logger.debug(f"Found all expected symbols after {scroll_attempts + 1} scroll attempts. Stopping early.")
                break

            # Check if we're not finding new symbols (end of list)
            if len(all_symbols) == last_count:
                logger.debug("No new symbols found in this scroll attempt")
                not_found_time += 1
                if set(all_symbols) == set(expected_symbols) or not_found_time == 5:
                    break
            else:
                not_found_time = 0
                last_count = len(all_symbols)

            # Scroll down in the container
            try:
                self._scroll_watchlist_container()
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

        res = self.actions.get_text_elements(self.__items)
        return res

    def get_random_symbol(self, tab=None):
        res = None
        cur_symbols = self.get_current_symbols(tab)
        if cur_symbols:
            res = random.choice(cur_symbols[:5 if len(cur_symbols) > 5 else int(len(cur_symbols)/2)])
            logger.debug(f"- Selected symbol: {res!r}")

        return res

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

    def select_symbol(self, symbol, tab=None, max_scroll_attempts=30):
        """Select symbol from current displayed list with enhanced scrolling
        Args:
            symbol: Symbol name to select
            tab: Tab to search in (optional)
            max_scroll_attempts: Maximum number of scroll attempts
        Raises:
            Exception: If symbol is not found after all attempts
        """
        if tab:
            self.select_tab(tab)

        logger.debug(f"Attempting to select symbol: {symbol!r}")
        locator = cook_element(self.__item_by_name, symbol)
        
        # First check if symbol is already visible
        if self.actions.is_element_displayed(locator):
            logger.debug(f"Symbol {symbol!r} is already visible, clicking immediately")
            self.actions.click(locator)
            return

        # Scroll to find the symbol
        scroll_attempts = 0
        
        while scroll_attempts < max_scroll_attempts:
            logger.debug(f"Scroll attempt {scroll_attempts + 1}/{max_scroll_attempts} to find symbol: {symbol!r}")
            
            # Scroll down in the container
            try:
                self._scroll_watchlist_container()
            except Exception as e:
                logger.warning(f"Error during scroll attempt {scroll_attempts + 1}: {e}")
                scroll_attempts += 1
                continue
            
            # Check if symbol is now visible
            if self.actions.is_element_displayed(locator):
                logger.debug(f"Symbol {symbol!r} found after {scroll_attempts + 1} scroll attempts")
                self.actions.click(locator)
                return
            
            scroll_attempts += 1
        
        raise Exception(f"Symbol '{symbol}' not found after {scroll_attempts} scroll attempts")

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
        actual_tabs = self.actions.get_text_elements(self.__all_tabs)
        soft_assert(sorted(actual_tabs), sorted(expected_tabs))

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

    def verify_symbols_displayed(self, symbols: str | list = None, is_display=True):
        """Verify symbol is displayed in tab"""

        symbols = symbols if isinstance(symbols, list) else [symbols]
        locator_list = [cook_element(self.__item_by_name, symbol) for symbol in symbols]
        self.actions.verify_elements_displayed(locator_list, timeout=SHORT_WAIT, is_display=is_display)

    def verify_symbols_list(self, tab=None, symbols=None):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        current_symbols = self.get_all_symbols(tab, expected_symbols=symbols)

        if len(current_symbols) > len(symbols):
            current_symbols = [item for item in current_symbols if item in symbols]

        soft_assert(
            sorted(current_symbols) == sorted(symbols), True,
            error_message=f"Missing: {[item for item in symbols if item not in current_symbols]}"
        )
