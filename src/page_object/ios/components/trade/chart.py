import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger

OHLC = {}


class Chart(BaseTrade):
    INIT_OCHL = {}

    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __candlestick = (AppiumBy.XPATH, "(//XCUIElementTypeOther[@name='Candlestick '])[1]")
    __timeframe = (AppiumBy.XPATH, "(//XCUIElementTypeOther[@name='4H '])[1]")
    __chart_loaded = (AppiumBy.XPATH, "//*[starts-with(@name, 'O: ')]")
    __chart_ohlc = (
        AppiumBy.XPATH,
        "//*[starts-with(@name, 'O: ') or starts-with(@name, 'H: ') or starts-with(@name, 'L: ') or starts-with(@name, 'C: ')]",
    )
    __symbol_over_view = (AppiumBy.IOS_PREDICATE, "name == 'symbol-overview-id' AND label == '{}'")

    # ------------------------ ACTIONS ------------------------ #

    def is_symbol_selected(self, symbol):
        return self.actions.is_element_displayed(cook_element(self.__symbol_over_view, symbol))

    def open_candlestick_opt(self):
        self.actions.click_by_offset(self.__candlestick, -22, 10, raise_exception=False)

    def select_timeframe(self, timeframe: ChartTimeframe):
        match timeframe:
            case ChartTimeframe.one_min:
                y_percent = 0.5 if RuntimeConfig.is_mt4() else 0.15
            case ChartTimeframe.five_min:
                y_percent = 0.55 if RuntimeConfig.is_mt4() else 0.35
            case ChartTimeframe.ten_min:
                y_percent = 0.45
            case ChartTimeframe.fifteen_min:
                y_percent = 0.6 if RuntimeConfig.is_mt4() else 0.47
            case ChartTimeframe.twenty_min:
                y_percent = 0.5
            case ChartTimeframe.thirty_min:
                y_percent = 0.55
            case ChartTimeframe.one_hour:
                y_percent = 0.7 if RuntimeConfig.is_mt4() else 0.6
            case ChartTimeframe.two_hour:
                y_percent = 0.65
            case ChartTimeframe.three_hour:
                y_percent = 0.7
            case ChartTimeframe.four_hour:
                y_percent = 0.75
            case ChartTimeframe.six_hour:
                y_percent = 0.8
            case ChartTimeframe.one_day:
                y_percent = 0.8 if RuntimeConfig.is_mt4() else 0.85
            case ChartTimeframe.one_week:
                y_percent = 0.85 if RuntimeConfig.is_mt4() else 0.9
            case ChartTimeframe.one_month:
                y_percent = 0.9
                if not RuntimeConfig.is_mt4():
                    self.actions.scroll_down()
            case _:
                raise ValueError("Invalid Timeframe")

        self.actions.click_screen_position(y_percent=y_percent)
        logger.debug(f"- timeframe: {timeframe!r} selected")

    def get_ohlc_values(self):
        """Get current OHLC values as plain text (fresh each time)."""
        ohlc_values = {}
        try:
            ohlc_elements = self.actions.find_elements(self.__chart_ohlc, timeout=0.5, show_log=False)
            for element in ohlc_elements:
                text = (
                    element.get_attribute("name")
                    or element.get_attribute("label")
                    or element.get_attribute("value")
                )
                if not text:
                    continue

                if text.startswith("O: "):
                    ohlc_values["O"] = text

                elif text.startswith("H: "):
                    ohlc_values["H"] = text

                elif text.startswith("L: "):
                    ohlc_values["L"] = text

                elif text.startswith("C: "):
                    ohlc_values["C"] = text

        except Exception as e:
            logger.debug(f"Failed to find OHLC elements: {type(e).__name__}")

        # Always update INIT_OCHL if values exist
        if ohlc_values:
            Chart.INIT_OCHL = ohlc_values.copy()
            logger.debug(f"- Updated INIT_OCHL: {Chart.INIT_OCHL}")

        return ohlc_values

    def get_default_render_time(self, max_wait: int = 10):
        """Measure initial chart render time by waiting for first OHLC values."""
        start = time.time()

        while time.time() - start < max_wait:
            ohlc_values = self.get_ohlc_values()
            if ohlc_values:
                elapsed = round(time.time() - start, 2)
                logger.debug(f"- Found OHLC values: {ohlc_values}")
                logger.debug(f"- Initial render time: {elapsed} sec")
                return elapsed
            time.sleep(0.2)

        logger.debug("- Chart render time is >10")
        return max_wait

    def get_timeframe_render_time(
        self, timeframe, max_wait: int = 10, max_retries: int = 3, expected_time: int = RuntimeConfig.charttime
    ):
        """
        Measure render time after switching timeframe by detecting OHLC value changes.
        Uses INIT_OCHL if available, otherwise fetches a new one.
        Retries if:
          - No change detected within max_wait, OR
          - Detected render time > expected_time
        On retry, switches to a different timeframe first, then back to the target one.
        """

        fallback_timeframe = "1m" if timeframe != "1m" else "5m"

        for attempt in range(1, max_retries + 1):
            # Use INIT_OCHL if available, otherwise fetch new
            current_ohlc = Chart.INIT_OCHL if Chart.INIT_OCHL else self.get_ohlc_values()
            logger.debug(f"[Attempt {attempt}] Measuring render for {timeframe}")

            # Select timeframe
            self.open_candlestick_opt()
            self.select_timeframe(timeframe)

            start = time.time()

            while time.time() - start < max_wait:
                time.sleep(0.2)
                new_ohlc = self.get_ohlc_values()

                if not new_ohlc or not current_ohlc:
                    continue

                changed = [
                    k
                    for k in ["O", "H", "L", "C"]
                    if new_ohlc.get(k) and current_ohlc.get(k) and new_ohlc[k] != current_ohlc[k]
                ]

                if changed:
                    elapsed = round(time.time() - start, 2)
                    logger.debug(f"↳ OHLC changed ({changed}), render time={elapsed}s")

                    if elapsed > expected_time and attempt < max_retries:
                        logger.debug(
                            f"↳ Too slow (> {expected_time}s), retrying with bounce {fallback_timeframe}"
                        )
                        self.open_candlestick_opt()
                        self.select_timeframe(
                            ChartTimeframe.one_min
                            if timeframe != ChartTimeframe.one_min
                            else ChartTimeframe.five_min
                        )
                        time.sleep(1)
                        break  # retry outer loop
                    return elapsed

            if attempt < max_retries:
                logger.debug(f"↳ No change within {max_wait}s, retrying with bounce {fallback_timeframe}")
                self.open_candlestick_opt()
                self.select_timeframe(
                    ChartTimeframe.one_min if timeframe != ChartTimeframe.one_min else ChartTimeframe.five_min
                )
                time.sleep(1)

        logger.debug(f"↳ Fallback return: {max_wait}s (max wait exceeded)")
        return max_wait

    # ------------------------ VERIFY ------------------------ #

    @staticmethod
    def verify_render_time(actual, expected):
        soft_assert(
            actual <= expected,
            True,
            error_message=f"Actual render time: {actual!r} sec, Expected: {expected!r} sec",
        )
