import re
import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class Chart(BaseTrade):

    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __candlestick = (AppiumBy.XPATH, "(//XCUIElementTypeOther[@name='Candlestick '])[1]")
    __symbol_over_view = (AppiumBy.IOS_PREDICATE, "name == 'symbol-overview-id' AND label == '{}'")
    __chart_open = (AppiumBy.XPATH, "//*[starts-with(@name, 'O: ')]")
    __chart_high = (AppiumBy.XPATH, "//*[starts-with(@name, 'H: ')]")
    __chart_low = (AppiumBy.XPATH, "//*[starts-with(@name, 'L: ')]")
    __chart_close = (AppiumBy.XPATH, "//*[starts-with(@name, 'C: ')]")
    __chart_timeframe_option = (AppiumBy.ACCESSIBILITY_ID, "chart-period-option-{}")

    # ------------------------ ACTIONS ------------------------ #

    def is_symbol_selected(self, symbol):
        return self.actions.is_element_displayed(cook_element(self.__symbol_over_view, symbol))

    def open_candlestick_opt(self):
        self.actions.click_by_offset(self.__candlestick, -22, 10, raise_exception=False)

    def _get_initial_ohlc_values(self):
        """
        Get initial OHLC values from chart elements.
        Assumes we have individual locators for O, H, L, C.
        Returns a dict: {"o": value, "h": value, "l": value, "c": value}
        """
        try:
            return {
                "o": self.actions.get_attribute(self.__chart_open, "name"),
                "h": self.actions.get_attribute(self.__chart_high, "name"),
                "l": self.actions.get_attribute(self.__chart_low, "name"),
                "c": self.actions.get_attribute(self.__chart_close, "name"),
            }
        except Exception as e:
            logger.error(f"Error getting initial OHLC values: {e}")
            return {"o": None, "h": None, "l": None, "c": None}

    # def select_timeframe(self, timeframe: ChartTimeframe):
    #     match timeframe:
    #         case ChartTimeframe.one_min:
    #             y_percent = 0.5 if RuntimeConfig.is_mt4() else 0.15
    #         case ChartTimeframe.five_min:
    #             y_percent = 0.55 if RuntimeConfig.is_mt4() else 0.35
    #         case ChartTimeframe.ten_min:
    #             y_percent = 0.43
    #         case ChartTimeframe.fifteen_min:
    #             y_percent = 0.6 if RuntimeConfig.is_mt4() else 0.47
    #         case ChartTimeframe.twenty_min:
    #             y_percent = 0.5
    #         case ChartTimeframe.thirty_min:
    #             y_percent = 0.55 if not RuntimeConfig.is_mt4() else 0.65
    #         case ChartTimeframe.one_hour:
    #             y_percent = 0.7 if RuntimeConfig.is_mt4() else 0.6
    #         case ChartTimeframe.two_hour:
    #             y_percent = 0.65
    #         case ChartTimeframe.three_hour:
    #             y_percent = 0.7
    #         case ChartTimeframe.four_hour:
    #             y_percent = 0.75
    #         case ChartTimeframe.six_hour:
    #             y_percent = 0.8
    #         case ChartTimeframe.one_day:
    #             y_percent = 0.8 if RuntimeConfig.is_mt4() else 0.85
    #         case ChartTimeframe.one_week:
    #             y_percent = 0.85 if RuntimeConfig.is_mt4() else 0.9
    #         case ChartTimeframe.one_month:
    #             y_percent = 0.9
    #             if not RuntimeConfig.is_mt4():
    #                 self.actions.scroll_down()
    #         case _:
    #             raise ValueError("Invalid Timeframe")
    #
    #     self.actions.click_screen_position(y_percent=y_percent)
    #     logger.debug(f"- timeframe: {timeframe!r} selected")

    def select_timeframe(self, timeframe: ChartTimeframe):
        locator = cook_element(self.__chart_timeframe_option, timeframe)
        if not self.actions.is_element_displayed(locator):
            self.actions.scroll_down()
        self.actions.click(locator)


    def get_default_render_time(self, max_wait: int = 10):
        """Measure initial chart render time by waiting for first OHLC values."""
        start = time.time()

        while time.time() - start < max_wait:
            self.actions.wait_for_element_visible(self.__chart_open)
            elapsed = round(time.time() - start, 2)
            logger.debug(f"- Initial render time: {elapsed} sec")
            return elapsed

        logger.debug("- Chart render time is >10")
        return max_wait


    def get_timeframe_render_time(self, timeframe):

        logger.debug(f"- Switching to timeframe: {timeframe}")
        init_o_value = self.actions.get_attribute(self.__chart_open, "name")

        self.open_candlestick_opt()
        self.select_timeframe(timeframe)
        elapsed = self._get_chart_render_time(init_o_value)

        return elapsed

    def _get_chart_render_time(self, init_o_value: str):
        """
        Measure time for 'O:' value to change in the chart.
        init_o_value: initial value of 'O:' (e.g., '25,202.48')
        Returns: elapsed time (float) or timeout (float)
        """
        timeout = 10
        poll_interval = 0.05
        start = time.time()
        sleep_time = 0

        # Precompile regex for better performance
        pattern = re.compile(r'name="O:\s([\d,.]+)"')

        logger.info("- Start calculating render time")
        while time.time() - start < timeout:
            xml = self.actions._driver.page_source

            # Extract O value
            match = pattern.search(xml)
            if match:
                current_o = f"O: {match.group(1)}"
                logger.debug(f"- Current O value: {current_o}")

                # Compare with initial value
                if current_o != init_o_value:
                    elapsed = round(time.time() - start, 2)
                    logger.debug(f"- O value changed from {init_o_value} to {current_o} -> elapsed: {elapsed!r}")
                    return elapsed

            time.sleep(poll_interval)
            sleep_time += poll_interval

        return timeout - sleep_time - 1

    # ------------------------ VERIFY ------------------------ #

    @staticmethod
    def verify_render_time(actual, expected):
        soft_assert(
            actual <= expected,
            True,
            error_message=f"Actual render time: {actual!r} sec, Expected: {expected!r} sec",
        )
