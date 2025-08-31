import random
import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
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

    __btn_symbol_preference = (AppiumBy.XPATH, "//android.view.ViewGroup[5]/android.view.ViewGroup")
    __symbol_preference = (AppiumBy.XPATH, "//android.widget.ScrollView//android.view.ViewGroup[@content-desc]")
    __chb_symbol_preference = (AppiumBy.XPATH, "//android.widget.ScrollView//android.widget.TextView[@text='{}']/preceding-sibling::android.view.ViewGroup[.//android.widget.TextView]")
    __unchb_show_all = (AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='Show all']/android.view.ViewGroup")
    __chb_show_all = (AppiumBy.XPATH, "//android.view.ViewGroup[contains(@content-desc, 'Show all')]/android.view.ViewGroup[android.widget.TextView]")
    __btn_save_changes = (AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='Save Changes']")

    # ------------------------ ACTIONS ------------------------ #

    def set_symbol_preference(self, tab: WatchListTab, unchecked=True, show_all=None, store_dict=None):
        """Show/Hide Symbols with accurate state detection"""

        logger.debug("Opening symbol preference setting")
        self.actions.wait_for_element_visible(self.__btn_symbol_preference)  # wait for the filter button to be visible
        self.actions.click(self.__btn_symbol_preference)

        time.sleep(1)  # Wait a bit to allow the tab to display
        self.watch_list.select_tab(tab)
        time.sleep(3)  # Wait a bit for symbol list to load

        elements = self.actions.find_elements(self.__symbol_preference)
        tmp = [ele.get_attribute("content-desc") for ele in elements]
        symbol_list = [item.split(",")[-1].strip() for item in tmp]

        # Sort the symbol list for consistency
        symbol_list.sort()

        logger.debug(f"Setting Show All preference to: {show_all}")

        if show_all is not None:
            locator = self.__unchb_show_all if show_all else self.__chb_show_all
            self.actions.click(locator)

        else:
            # Randomly select number of symbols to modify
            random_amount = random.randint(1, len(symbol_list) - 1) if symbol_list else 0

            for symbol in symbol_list[:random_amount]:
                checked_locator = cook_element(self.__chb_symbol_preference, symbol)
                is_checked = self.actions.is_element_displayed(checked_locator)

                # Determine if action is needed
                if (unchecked and is_checked) or (not unchecked and not is_checked):
                    action = "unchecked" if unchecked else "checked"
                    logger.debug(f"- {action} symbol: {symbol!r}")
                    self.actions.click(checked_locator)
                    time.sleep(0.5)

        # Store results if dictionary provided
        if store_dict is not None and symbol_list:
            store_dict |= {
                "hide": symbol_list[:random_amount],
                "show": symbol_list[random_amount:]
            }

        # Save changes if save button is enabled
        if self.actions.is_element_enabled(self.__btn_save_changes, timeout=QUICK_WAIT):
            logger.debug("- Click on btn save changes")
            self.actions.click(self.__btn_save_changes)
            time.sleep(1)  # wait a bit

    # ------------------------ VERIFY ------------------------ #
