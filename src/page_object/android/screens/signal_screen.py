from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import SignalTab
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.base_screen import BaseScreen
from src.utils.common_utils import resource_id
from src.utils.logging_utils import logger


class SignalScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

        # ------------------------ LOCATORS ------------------------ #
        self.__tab_favourite = (AppiumBy.XPATH, "//android.widget.TextView[@text='Favourite']")
        self.__tab_signal_list = (AppiumBy.XPATH, "//android.widget.TextView[@text='All']")
        self.__btn_add_favourite = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Add to favourites']")
        self.__btn_remove_favourite = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Remove from favourites']")
        self.__btn_copy_signal = (AppiumBy.XPATH, "//android.widget.Button[@text='Copy']")
        self.__signal_item = (AppiumBy.XPATH, resource_id('signal-item'))
        self.__signal_symbol = (AppiumBy.XPATH, resource_id('signal-symbol'))
        self.__signal_items = (AppiumBy.XPATH, resource_id('signal-list'))

    # ------------------------ ACTIONS ------------------------ #
    def select_tab(self, tab: SignalTab) -> None:
        """Select signal tab (Favourite or All)."""
        logger.debug(f"- Select {tab!r} tab")
        tab_locator = self.__tab_favourite if tab == SignalTab.FAVOURITE else self.__tab_signal_list
        self.actions.click(tab_locator)

    def add_signal_to_favourites(self) -> str:
        """Add first available signal to favourites and return signal ID."""
        logger.debug("- Add signal to favourites")
        signal_elements = self.actions.find_elements(self.__signal_item)
        if not signal_elements:
            raise Exception("No signals found to add to favourites")
        
        signal_element = signal_elements[0]
        signal_id = signal_element.get_attribute("content-desc") or f"signal_{len(signal_elements)}"
        
        # Click add to favourites button within the signal item
        self.actions.click(self.__btn_add_favourite)
        return signal_id

    def remove_signal_from_favourites(self, signal_id: str) -> None:
        """Remove signal from favourites."""
        logger.debug(f"- Remove signal {signal_id!r} from favourites")
        self.actions.click(self.__btn_remove_favourite)

    def select_signal_for_copy(self) -> dict:
        """Select a signal and return its data for copying."""
        logger.debug("- Select signal for copy")
        signal_elements = self.actions.find_elements(self.__signal_item)
        if not signal_elements:
            raise Exception("No signals found to copy")
        
        signal_element = signal_elements[0]
        signal_id = signal_element.get_attribute("content-desc") or f"signal_{len(signal_elements)}"
        
        # Try to get symbol from signal element or use default
        try:
            symbol_element = self.actions.find_element(self.__signal_symbol)
            symbol = symbol_element.text if symbol_element else "EURUSD"
        except:
            symbol = "EURUSD"
        
        signal_data = {
            "symbol": symbol,
            "signal_id": signal_id
        }
        
        self.actions.click(signal_element)
        return signal_data

    def copy_signal_to_order(self, signal_data: dict) -> ObjTrade:
        """Copy signal to trade order and return trade object."""
        logger.debug(f"- Copy signal {signal_data['signal_id']!r} to order")
        self.actions.click(self.__btn_copy_signal)
        
        # Create trade object with signal data
        trade_object = ObjTrade(symbol=signal_data["symbol"])
        return trade_object

    # ------------------------ VERIFY ------------------------ #
    def verify_signal_in_favourites(self, signal_id: str) -> None:
        """Verify signal is displayed in favourites tab."""
        logger.debug(f"- Verify signal {signal_id!r} in favourites")
        signal_locator = (AppiumBy.XPATH, f"{resource_id('signal-item')}[@content-desc='{signal_id}']")
        assert self.actions.is_element_displayed(signal_locator), f"Signal {signal_id} not found in favourites"

    def verify_signal_not_in_favourites(self, signal_id: str) -> None:
        """Verify signal is not displayed in favourites tab."""
        logger.debug(f"- Verify signal {signal_id!r} not in favourites")
        signal_locator = (AppiumBy.XPATH, f"{resource_id('signal-item')}[@content-desc='{signal_id}']")
        assert not self.actions.is_element_displayed(signal_locator), f"Signal {signal_id} still found in favourites"
