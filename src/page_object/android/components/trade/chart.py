import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import EXPLICIT_WAIT
from src.data.enums import ChartTimeframe
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class Chart(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __candle_stick = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Candlestick')]")
    __chart_timeframe_option = (AppiumBy.XPATH, "//android.widget.TextView[@text='{}']")
    __chart_loading = (AppiumBy.XPATH, "//android.view.View[@resource-id='chart-root']/android.widget.TextView[1]")

    # ------------------------ ACTIONS ------------------------ #

    def open_timeframe_opt(self):
        self.actions.click_by_offset(self.__candle_stick, x_offset=-30)

    def select_timeframe(self, timeframe: ChartTimeframe):
        self.open_timeframe_opt()

        locator = cook_element(self.__chart_timeframe_option, timeframe.locator_map())
        if not self.actions.is_element_displayed(locator):
            self.actions.scroll_down()
        self.actions.click(locator)

    def get_default_render_time(self):
        start = time.time()
        self.actions.wait_for_element_invisible(self.__chart_loading)
        elapsed = round(time.time() - start, 2)
        logger.debug(f"- Render time: {elapsed} sec")
        return elapsed

    def get_timeframe_render_time(self, timeframe):
        self.select_timeframe(timeframe)
        start = time.time()
        self.actions.wait_for_element_invisible(self.__chart_loading, timeout=EXPLICIT_WAIT)
        elapsed = round(time.time() - start, 2)
        logger.debug(f"- Render time: {elapsed} sec")

        return elapsed
    # ------------------------ VERIFY ------------------------ #

    @staticmethod
    def verify_render_time(actual, expected):
        soft_assert(actual <= expected, True, error_message=f"Actual render time: {actual!r} sec, Expected: {expected!r} sec")
