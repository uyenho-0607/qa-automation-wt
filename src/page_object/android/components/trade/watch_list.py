import random
from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.data.enums import WatchListTab
from src.utils import DotDict
from src.utils.common_utils import resource_id, cook_element


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
        locator = cook_element(self.__tab, tab)
        
        if tab == WatchListTab.FAVOURITES and self.actions.is_element_displayed(locator):
            self.actions.click(locator)
            return
            
        # If not visible, attempt to scroll horizontally to reveal it
        if not self.actions.is_element_displayed(locator):
            self.actions.scroll_direction()
        self.actions.click(locator)


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

    def select_last_symbol(self, tab: WatchListTab = WatchListTab.ALL):
        self.select_tab(tab)
        self.actions.click(self.__items)

    
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
            self.actions.click(locator) # click on the symbol name
            self.actions.click(self.__star_icon_by_symbol) # click on the star icon
            self.go_back()

        else:
            self.actions.swipe_left_on_element(locator) # swipe left action
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