import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
from src.data.enums import ChartTimeframe
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger


class Chart(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __candlestick = (AppiumBy.XPATH, "(//XCUIElementTypeOther[@name='Candlestick '])[1]")
    __timeframe = (AppiumBy.XPATH, "(//XCUIElementTypeOther[@name='4H '])[1]")
    __chart_loaded = (AppiumBy.XPATH, "//*[starts-with(@name, 'O: ')]")

    # ------------------------ ACTIONS ------------------------ #
    def open_candlestick_opt(self):
        self.actions.click_by_offset(self.__candlestick, -22, 10, raise_exception=False)

    def select_timeframe(self, timeframe: ChartTimeframe):
        match timeframe:
            case ChartTimeframe.one_min:
                y_percent = 0.15
            case ChartTimeframe.five_min:
                y_percent = 0.2
            case ChartTimeframe.ten_min:
                y_percent = 0.25
            case ChartTimeframe.fifteen_min:
                y_percent = ...
            case ChartTimeframe.twenty_min:
                y_percent = 0.3
            case ChartTimeframe.thirty_min:
                y_percent = 0.35
            case ChartTimeframe.one_hour:
                y_percent = 0.4
            case ChartTimeframe.two_hour:
                y_percent = 0.45
            case ChartTimeframe.three_hour:
                y_percent = 0.5
            case ChartTimeframe.four_hour:
                y_percent = 0.55
            case ChartTimeframe.six_hour:
                y_percent = 0.6
            case ChartTimeframe.one_day:
                y_percent = 0.7
            case ChartTimeframe.one_week:
                y_percent = 0.75
            case ChartTimeframe.one_month:
                y_percent = 0.8
            case _:
                raise ValueError("Invalid Timeframe")

        self.actions.click_screen_position(y_percent=y_percent)
        breakpoint()
        logger.debug(f"- timeframe: {timeframe!r} selected")

    def get_default_render_time(self):
        start = time.time()
        self.actions.wait_for_element_visible(self.__chart_loaded)
        elapsed = time.time() - start

        logger.debug(f"- Render time: {elapsed} sec")
        return round(elapsed, 2)

    def get_timeframe_render_time(self, timeframe):
        # Get initial O value
        current_o_value = self.actions.get_attribute(self.__chart_loaded, "value")
        logger.debug(f"Initial O value: {current_o_value}")

        # Select timeframe
        logger.debug(f"- Select timeframe: {timeframe!r}")
        self.open_candlestick_opt()
        self.select_timeframe(timeframe)

        start = time.time()

        # Wait for O value to change
        while time.time() - start < 10:
            logger.debug("- Wait for chart load new 'O' value...")
            time.sleep(0.1)
            new_o_value = self.actions.get_attribute(self.__chart_loaded, "value", timeout=QUICK_WAIT)
            if new_o_value != current_o_value:
                elapsed = time.time() - start
                logger.debug(f"- New 'O' value: {new_o_value}")
                logger.debug(f"- Chart render time for {timeframe}: {round(elapsed, 2)} sec")
                return elapsed

        logger.debug("- Take too long for chart render, > 10 sec")
        return 10

    # ------------------------ VERIFY ------------------------ #

    @staticmethod
    def verify_render_time(actual, expected):
        soft_assert(actual <= expected, True, error_message=f"Actual render time: {actual!r} sec, Expected: {expected!r} sec")
