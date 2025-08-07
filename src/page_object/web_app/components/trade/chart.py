from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.data.enums.trading import ChartTimeframe
from src.page_object.web_app.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid


class Chart(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __chart_toggle_fullscreen = (By.CSS_SELECTOR, data_testid('chart-toggle-fullscreen'))
    __chart_exit_fullscreen = (By.CSS_SELECTOR, data_testid('chart-exit-fullscreen'))
    __tab_trade = (By.CSS_SELECTOR, data_testid('tab-trade'))
    __btn_close_trade = (By.CSS_SELECTOR, data_testid('chart-trade-button-close'))
    __timeframe_selector = (By.XPATH, "//div[text()='{}']")
    __symbol_overview = (By.XPATH, "//div[@data-testid='symbol-overview-id' and contains(text(), '{}')]")

    # ------------------------ ACTIONS ------------------------ #
    def toggle_chart(self, fullscreen=True, timeout=SHORT_WAIT):

        if fullscreen and self.actions.is_element_displayed(self.__chart_toggle_fullscreen, timeout=timeout):
            self.actions.click(self.__chart_toggle_fullscreen)

        if not fullscreen and self.actions.is_element_displayed(self.__chart_exit_fullscreen, timeout=timeout):
            self.actions.click(self.__chart_exit_fullscreen)

    def open_trade_tab(self):
        self.actions.click(self.__tab_trade)

    def close_trade_tab(self):
        self.actions.click(self.__btn_close_trade)

    def select_timeframe(self, timeframe: ChartTimeframe):
        self.actions.click(cook_element(self.__timeframe_selector, timeframe))

    # ------------------------ VERIFY ------------------------ #

    def verify_timeframe_selected(self, timeframe: ChartTimeframe):
        locator = cook_element(self.__timeframe_selector, timeframe)
        is_selected = "selected" in self.actions.get_attribute(locator, "class")
        soft_assert(is_selected, True, error_message=f"Timeframe {timeframe.title()} is not selected")

    def verify_symbol_selected(self, symbol):
        self.actions.verify_element_displayed(cook_element(self.__symbol_overview, symbol))
