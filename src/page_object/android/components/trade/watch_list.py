import random

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import WatchListTab
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id, cook_element
from src.utils.logging_utils import logger


class WatchList(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, '{}')]")
    __items = (AppiumBy.XPATH, resource_id('watchlist-symbol'))
    __item_by_name = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='watchlist-symbol' and @text='{}']")
    __star_icon_by_symbol = (AppiumBy.XPATH, resource_id("chart-star-symbol"))
    __btn_symbol_remove = (AppiumBy.XPATH, "//*[@text='Remove']")
    __selected_item = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='symbol-overview-id' and @text='{}']")

    # ------------------------ ACTIONS ------------------------ 

    def select_tab(self, tab: WatchListTab):
        """Handle selecting tab for home & markets screen"""
        locator = cook_element(self.__tab, tab)

        logger.info(f"- Select tab: {tab.value.capitalize()!r}")
        # if tab is represent, select tab immediately
        if self.actions.is_element_displayed(locator):
            self.actions.click(locator)
            return

        # For home screen, in case tab is sub-tab
        logger.debug(f"- Tab is sub-tab, select tab {WatchListTab.ALL.value!r} first")
        self.actions.click(cook_element(self.__tab, WatchListTab.ALL))
        self.actions.click(locator)

    def get_current_symbols(self, tab: WatchListTab = None, random_symbol=False):
        if tab:
            self.select_tab(tab)

        elements = self.actions.find_elements(self.__items)
        if elements:
            res = [ele.text.strip() for ele in elements]
            res = [item for item in res if item]  # remove empty text if any
            return res if not random_symbol else random.choice(res)

        return []

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

    def get_all_symbols(self, tab: WatchListTab = None, expected_symbols=None):
        if tab:
            self.select_tab(tab)

        all_symbols = set()
        scroll_attempts = 0
        last_count = 0
        max_scroll_attempts: int = int(len(expected_symbols) / 2)
        no_new_symbol = 0
        # logger.debug(f"- Max scroll attempts: {max_scroll_attempts!r}")

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
                no_new_symbol +=1
                if set(all_symbols) == set(expected_symbols) or no_new_symbol == 5:
                    break
            else:
                no_new_symbol = 0
                last_count = len(all_symbols)

            # Scroll down in the container
            try:
                self.actions.scroll_down(scroll_step=0.4)
                # self.actions.scroll_container_down(self.__watchlist_container, scroll_step=0.5)
            except Exception as e:
                logger.warning(f"Error during scroll: {e}")
                break

            scroll_attempts += 1

        result = list(all_symbols)
        logger.debug(f"Finished scrolling. Total symbols collected: {len(result)}")
        return result

    def select_last_symbol(self, tab: WatchListTab = WatchListTab.ALL):
        if tab:
            self.select_tab(tab)

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

            # Scroll down in the container
            try:
                self.actions.scroll_down()
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

    def toggle_star_symbol(self, mark_star=True):
        """
        To either mark a symbol as favorite or remove it from favorites.
        :param mark_star: True to mark star, False to remove from favorites.
        """

        items = self.actions.find_elements(self.__items)
        symbols = [item.get_attribute("text") for item in items]
        selected_symbol = random.choice(symbols)

        locator = cook_element(self.__item_by_name, selected_symbol)

        if mark_star:
            self.actions.click(locator)  # click on the symbol name
            self.actions.click(self.__star_icon_by_symbol)  # click on the star icon
            self.go_back()

        else:
            self.actions.swipe_element_horizontal(locator)  # swipe left action
            self.actions.click(self.__btn_symbol_remove)

        return selected_symbol

    # ------------------------ VERIFY ------------------------ #

    def verify_symbol_selected(self, symbol: str):
        """Verify selected item"""
        self.actions.verify_element_displayed(cook_element(self.__selected_item, symbol))

    def verify_symbols_displayed(self, tab: WatchListTab, symbols: str | list = None, is_display=True, timeout=SHORT_WAIT):
        """Verify symbol is displayed in tab"""
        self.select_tab(tab)
        symbols = symbols if isinstance(symbols, list) else [symbols]
        for symbol in symbols:
            self.actions.verify_element_displayed(cook_element(self.__item_by_name, symbol), is_display=is_display, timeout=timeout)

    def verify_symbols_list(self, symbols, tab=None):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        current_symbols = self.get_all_symbols(tab, expected_symbols=symbols)

        soft_assert(
            sorted(current_symbols), sorted(symbols),
            error_message=f"Missing: {[item for item in symbols if item not in current_symbols]}, Redundant: {[item for item in current_symbols if item not in symbols]}"
        )