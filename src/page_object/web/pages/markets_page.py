import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT
from src.data.enums import MarketsSection, WatchListTab, TradeType
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.trade.watch_list import WatchList
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger


class MarketsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __symbol_row = (By.CSS_SELECTOR, data_testid('{}-symbol'))  # symbol-row from MarketsSection
    __symbol_row_text = (By.XPATH, "//div[@data-testid='{}-symbol' and text()='{}']")

    # __my_trade_symbol = (By.CSS_SELECTOR, data_testid('portfolio-row-symbol'))
    # __my_trade_symbol_by_text = (By.XPATH, "//div[@data-testid='portfolio-row-symbol' and text()='{}']")
    # __my_trade_order_type = (By.CSS_SELECTOR, data_testid('portfolio-row-order-type'))
    #
    # __top_picks_symbol = (By.CSS_SELECTOR, data_testid('top-picks-symbol'))
    # __top_picks_symbol_by_text = (By.XPATH, "//div[@data-testid='top-picks-symbol' and text()='{}']")
    #
    # __top_gainer_symbol = (By.CSS_SELECTOR, data_testid('top-gainer-symbol'))
    # __top_gainer_symbol_by_text = (By.XPATH, "//div[@data-testid='top-gainer-symbol' and text()='{}']")
    #
    # __signal_symbol = (By.CSS_SELECTOR, data_testid('signal-row-symbol'))
    # __signal_symbol_by_text = (By.XPATH, "//div[@data-testid='signal-row-symbol' and text()='{}']")

    __news_content = (By.CSS_SELECTOR, data_testid('market-news-content-text'))

    __redirect_arrow = (
        By.XPATH,
        "//span[@data-testid='market-section-title' and text()='{}']"
        "/ancestor::div/*[@data-testid='market-section-show-more']"
    )
    __btn_symbol_preference = (By.CSS_SELECTOR, data_testid('symbol-preference'))
    __chb_show_all = (
        By.XPATH, "//div[@data-testid='symbol-preference-select-all-{}']//div"
    )
    __chb_symbol_preference = (
        By.XPATH, "//div[contains(@data-testid, 'symbol-preference-option-{}') and text()='{}']//div"
        # checked or unchecked
    )
    __symbol_preference = (By.XPATH, "//div[@data-testid='symbol-preference-options']/div")
    __btn_save_changes = (By.CSS_SELECTOR, data_testid('symbol-preference-save'))
    __btn_close_preference = (By.CSS_SELECTOR, data_testid('symbol-preference-close'))

    # ------------------------ ACTIONS ------------------------ #
    def get_symbols(self, section: MarketsSection):
        symbols = self.actions.get_text_elements(cook_element(self.__symbol_row, locator_format(section.symbol_row())))
        return symbols

    def click_arrow_icon(self, arrow: MarketsSection):
        self.actions.click(cook_element(self.__redirect_arrow, arrow))

    def select_symbol(self, section: MarketsSection | str, symbol: str = ""):
        """Select latest symbol from Section"""
        locator = self.__symbol_row if not symbol else self.__symbol_row_text

        logger.debug(f"- Select symbol {symbol} from section: {section!r}")
        self.actions.click(cook_element(locator, locator_format(section.symbol_row()), symbol))

        if not symbol:
            # GET and return the selected symbol
            symbol = self.actions.get_text(cook_element(locator, locator_format(section.symbol_row())))

        return symbol

    def select_news_content(self):
        self.actions.click(self.__news_content)

    def set_symbol_preference(
            self, tab: WatchListTab, unchecked=True, show_all=False,
            store_dict=None
    ):
        self.watch_list.select_tab(tab, wait=False)
        self.actions.click(self.__btn_symbol_preference)
        time.sleep(1)  # wait a bit
        custom = "checked" if unchecked else "unchecked"

        elements = self.actions.find_elements(self.__symbol_preference)
        symbol_list = sorted(ele.text.strip() for ele in elements)

        if show_all and self.actions.is_element_displayed(cook_element(self.__chb_show_all, custom)):
            logger.debug("- Check/ Uncheck Show All")
            self.actions.click(cook_element(self.__chb_show_all, custom))

            if store_dict is not None:
                store_dict |= {"symbol": symbol_list}

        else:
            max_amount = 5 if len(symbol_list) > 5 else len(symbol_list) - 1
            random_amount = random.randint(1, max_amount) if symbol_list else 0

            for symbol in symbol_list[:random_amount]:
                locator = cook_element(self.__chb_symbol_preference, custom, symbol)

                if unchecked and self.actions.is_element_displayed(locator):
                    logger.debug(f"- Uncheck symbol: {symbol!r}")
                    self.actions.click(locator)

                if not unchecked and self.actions.is_element_displayed(locator):
                    logger.debug(f"- Check symbol: {symbol!r}")
                    self.actions.click(locator)

            if store_dict is not None and symbol_list:
                store_dict |= {
                    "hide": symbol_list[:random_amount],
                    "show": symbol_list[random_amount:]
                }

        if self.actions.is_element_enabled(self.__btn_save_changes, timeout=QUICK_WAIT):
            logger.debug("- Click on btn save changes")
            self.actions.click(self.__btn_save_changes)
            time.sleep(1)  # wait a bit

        logger.debug("- Close symbol preference setting")
        self.actions.click(cook_element(self.__btn_close_preference))

    # ------------------------ VERIFY ------------------------ #
    def verify_my_trade_list(self, symbols: str | list):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        actual = self.get_symbols(MarketsSection.MY_TRADE)
        soft_assert(actual, symbols)
