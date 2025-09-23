import random

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import WatchListTab
from src.page_object.ios.base_screen import BaseScreen
from src.page_object.ios.components.trade.watch_list import WatchList
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class MarketsScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #

    __tab = (AppiumBy.ACCESSIBILITY_ID, "{}")
    __items = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther[`name MATCHES '.*(SHARES|INDICES|CRYPTO|CMDTY|FOREX).*'`]")
    __item_by_name = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`label CONTAINS '{}'`][-1]")

    # ------------------------ ACTIONS ------------------------ #

    def select_tab(self, tab: WatchListTab):
        """Handle selecting tab for markets screen"""
        locator = cook_element(self.__tab, tab)
        logger.info(f"- Select tab: {tab.value.capitalize()!r}")
        self.actions.click(locator)

    def get_current_symbols(self, random_symbol=False):
        res = self.actions.get_text_elements(self.__items)
        extracted_symbols = [
            next(word for word in item.split() if word[0].isalnum() and word != "REMOVE")
            for item in res
        ]
        return extracted_symbols if not random_symbol else random.choice(extracted_symbols)

    def get_random_symbol(self):
        cur_symbols = self.get_current_symbols()
        return random.choice(cur_symbols[:5 if len(cur_symbols) > 5 else int(len(cur_symbols) / 2)])

    def select_symbol(self, symbol, max_scroll_attempts=30):
        """Select symbol from current displayed list with enhanced scrolling
        Args:
            symbol: Symbol name to select
            tab: Tab to search in (optional)
            max_scroll_attempts: Maximum number of scroll attempts
        Raises:
            Exception: If symbol is not found after all attempts
        """

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

    # ------------------------ VERIFY ------------------------ #
