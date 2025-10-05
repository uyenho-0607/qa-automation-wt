import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.data.enums import WatchListTab
from src.page_object.web_app.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.logging_utils import logger


class WatchList(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (By.XPATH, "//div[text()='{}']") # todo: change parent tabs to use data-testid
    __items = (By.CSS_SELECTOR, data_testid("watchlist-symbol"))
    __item_by_name = (By.XPATH, "//div[@data-testid='watchlist-symbol' and text()='{}']")
    __star_icon_by_symbol = (By.XPATH, data_testid("chart-star-symbol"))
    __btn_symbol_remove = (By.XPATH, "//*[text()='Remove']")
    __watchlist_container = (By.XPATH, "//div[@data-testid='watchlist-list-item']/ancestor::div[3]")

    # ------------------------ ACTIONS ------------------------ 
    def select_tab(self, tab: WatchListTab, wait=True, timeout=3):
        locator = cook_element(self.__tab, tab)
        max_retries = 3
        is_display = self.actions.is_element_displayed(locator, timeout=timeout)

        while not is_display and max_retries:
            logger.debug("- Tab is subtab, select tab ALL first")
            # self.actions.click(cook_element(self.__tab, WatchListTab.ALL))
            self.actions.javascript_click(cook_element(self.__tab, WatchListTab.ALL))
            self.wait_for_spin_loader()
            max_retries -= 1
            is_display = self.actions.is_element_displayed(locator)

        self.actions.click(locator)
        not wait or self.wait_for_spin_loader()

    def get_current_symbols(self):
        res = self.actions.get_text_elements(self.__items)
        return res

    def get_random_symbol(self):
        cur_symbols = self.get_current_symbols()
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

    def get_all_symbols(self, expected_symbols=None):
        all_symbols = set()
        scroll_attempts = 0
        last_count = 0
        max_scroll_attempts = int(len(expected_symbols) / 2) if len(expected_symbols) > 10 else 100
        no_new_symbol = 0

        while scroll_attempts < max_scroll_attempts:
            # Get current visible symbols
            current_symbols = self.get_current_symbols()

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
                no_new_symbol += 1
                if set(all_symbols) == set(expected_symbols) or no_new_symbol == 5:
                    break
            else:
                no_new_symbol = 0
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

    def select_last_symbol(self):
        self.actions.click(self.__items)

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
            time.sleep(2)

            # Scroll down in the container
            try:
                self.actions.scroll_container_down(self.__watchlist_container, scroll_step=0.5)
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

    # ------------------------ VERIFY ------------------------ #
    def verify_symbols_displayed(self, symbols: str | list = None, is_display=True, timeout=SHORT_WAIT):
        """Verify symbol is displayed in tab"""
        symbols = symbols if isinstance(symbols, list) else [symbols]
        locators = [cook_element(self.__item_by_name, _symbol) for _symbol in symbols]
        self.actions.verify_elements_displayed(locators, timeout=timeout, is_display=is_display)

    def verify_symbols_list(self, symbols):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        current_symbols = self.get_all_symbols(expected_symbols=symbols)

        soft_assert(
            sorted(item for item in current_symbols if item in symbols), sorted(symbols),
            error_message=f"Missing: {[item for item in symbols if item not in current_symbols]}"
        )
