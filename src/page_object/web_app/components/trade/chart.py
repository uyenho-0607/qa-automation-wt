import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.data.enums.trading import ChartTimeframe
from src.page_object.web_app.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.logging_utils import logger


class Chart(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __chart_toggle_fullscreen = (By.CSS_SELECTOR, data_testid('chart-toggle-fullscreen'))
    __chart_exit_fullscreen = (By.CSS_SELECTOR, data_testid('chart-exit-fullscreen'))
    __tab_trade = (By.CSS_SELECTOR, data_testid('tab-trade'))
    __btn_close_trade = (By.CSS_SELECTOR, data_testid('chart-trade-button-close'))
    __symbol_overview = (By.XPATH, "//div[@data-testid='symbol-overview-id' and contains(text(), '{}')]")
    __timeframe_selector = (By.XPATH, "//div[text()='{}']")
    __candle_stick = (By.XPATH, "//div[text()='Candlestick']")
    __chart_container = (By.XPATH, "//*[@id='chart-root']//div[@class='fullscreen-loader-container']")

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

    def open_timeframe_opt(self):
        self.actions.click_by_offset(self.__candle_stick, x_offset=-50)

    def is_symbol_selected(self, symbol, timeout=5):
        res = self.actions.wait_for_element_visible(cook_element(self.__symbol_overview, symbol), timeout=timeout)
        return res

    def select_timeframe(self, timeframe: ChartTimeframe):
        # Switch to main frame to ensure requests are captured
        self.actions.switch_to_default()
        self.open_timeframe_opt()

        logger.debug(f"- Select Timeframe: {timeframe!r}")
        locator = cook_element(self.__timeframe_selector, timeframe.locator_map())
        if self.actions.is_element_displayed(locator):
            self.actions.click(locator)
            return

        self.actions.scroll_to_element(locator)
        self.actions.click(locator)

    def _get_render_time(self):
        # Switch to iframe for checking loading state
        self.actions.switch_to_iframe()
        start = time.time()
        try:
            self.actions._wait.until(
                lambda d: "display: none;" == d.find_element(*self.__chart_container).get_attribute("style"),
                message="Chart container still showing loading state after timeout"
            )

            elapsed = round(time.time() - start, 2)

        except TimeoutError:
            logger.warning("- Timeout exceeds 10 sec")
            elapsed = 10

        # Switch back to main frame to ensure requests are captured
        self.actions.switch_to_default()
        return elapsed

    def get_default_render_time(self):
        return self._get_render_time()

    def get_timeframe_render_time(self, timeframe):
        # Switch to main frame before selecting timeframe
        self.actions.switch_to_default()
        self.select_timeframe(timeframe)
        return self._get_render_time()

    def exit_chart_iframe(self):
        self.actions.switch_to_default()

    # ------------------------ VERIFY ------------------------ #

    def verify_timeframe_selected(self, timeframe: ChartTimeframe):
        locator = cook_element(self.__timeframe_selector, timeframe)
        is_selected = "selected" in self.actions.get_attribute(locator, "class")
        soft_assert(is_selected, True, error_message=f"Timeframe {timeframe.title()} is not selected")

    def verify_symbol_selected(self, symbol):
        self.actions.verify_element_displayed(cook_element(self.__symbol_overview, symbol))

    @staticmethod
    def verify_render_time(actual, expected):
        soft_assert(actual <= expected, True, error_message=f"Actual render time: {actual!r} sec, Expected: {expected!r} sec")