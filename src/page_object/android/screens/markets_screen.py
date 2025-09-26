import random
import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import WatchListTab
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.trade.watch_list import WatchList
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class MarketsScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #

    __tab = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, '{}')]")
    __item_by_name = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='watchlist-symbol' and @text='{}']")
    __horizontal_scroll_tab = (AppiumBy.XPATH, "//android.widget.HorizontalScrollView")
    __btn_symbol_preference = (AppiumBy.XPATH, "//android.view.ViewGroup[5]/android.view.ViewGroup")
    __symbol_preference = (AppiumBy.XPATH, "//android.widget.ScrollView//android.view.ViewGroup[@content-desc]")
    __chb_symbol_preference = (AppiumBy.XPATH, "//android.widget.ScrollView//android.widget.TextView[@text='{}']/preceding-sibling::android.view.ViewGroup[.//android.widget.TextView]")
    __chb_show_all = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Show all").childSelector(new UiSelector().className("android.view.ViewGroup")).childSelector(new UiSelector().className("android.widget.TextView"))')
    __show_all_option = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Show all")')
    __btn_save_changes = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionMatches("(?i)save changes")')

    # ------------------------ ACTIONS ------------------------ #

    def select_tab(self, tab: WatchListTab):
        """Handle selecting tab for home & markets screen"""
        locator = cook_element(self.__tab, tab)

        logger.info(f"- Select tab: {tab.value.capitalize()!r}")
        # if tab is represent, select tab immediately
        if self.actions.is_element_displayed(locator):
            self.actions.click(locator)
            return

        # Handle swipe scroll tab for markets screen
        if self.actions.is_element_enabled(self.__horizontal_scroll_tab):
            # If not visible, attempt to scroll horizontally to reveal it
            for direction in ["left", "right"]:
                logger.debug(f"- Swipe {direction} to show tab")
                self.actions.swipe_element_horizontal(self.__horizontal_scroll_tab, direction)
                if self.actions.is_element_displayed(locator):
                    self.actions.click(locator)
                    return

    def set_symbol_preference(self, tab: WatchListTab, unchecked=True, show_all=None, store_dict=None):
        """Show/Hide Symbols with accurate state detection"""

        logger.debug("Opening symbol preference setting")
        self.actions.wait_for_element_visible(self.__btn_symbol_preference)  # wait for the filter button to be visible
        self.actions.click(self.__btn_symbol_preference)

        time.sleep(1)  # Wait a bit to allow the tab to display
        self.select_tab(tab)
        time.sleep(3)  # Wait a bit for symbol list to load

        elements = self.actions.find_elements(self.__symbol_preference)
        tmp = [ele.get_attribute("content-desc") for ele in elements]
        symbol_list = [item.split(",")[-1].strip() for item in tmp]

        # Sort the symbol list for consistency
        symbol_list.sort()

        logger.debug(f"Setting Show All preference to: {show_all}")

        if show_all is not None:
            is_show_all_checked = self.actions.is_element_displayed(self.__chb_show_all, timeout=SHORT_WAIT)
            logger.debug(f"Current Show All state: {is_show_all_checked}")

            if show_all != is_show_all_checked:
                logger.debug(f"Toggling Show All checkbox to: {show_all}")
                self.actions.click(self.__show_all_option)
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

    def verify_symbols_displayed(self, tab: WatchListTab, symbols: str | list = None, is_display=True, timeout=SHORT_WAIT):
        """Verify symbol is displayed in tab"""
        self.select_tab(tab)
        symbols = symbols if isinstance(symbols, list) else [symbols]
        for symbol in symbols:
            self.actions.verify_element_displayed(cook_element(self.__item_by_name, symbol), is_display=is_display, timeout=timeout)
