import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import MarketsSection, WatchListTab, TradeType
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.trade.watch_list import WatchList
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element
from src.utils.logging_utils import logger


class MarketsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __my_trade_symbol = (By.CSS_SELECTOR, data_testid('portfolio-row-symbol'))
    __my_trade_order_type = (By.CSS_SELECTOR, data_testid('portfolio-row-order-type'))
    __top_picks_symbol = (By.CSS_SELECTOR, data_testid('top-picks-symbol'))
    __top_gainer_symbol = (By.CSS_SELECTOR, data_testid('top-gainer-symbol'))
    __signal_symbol = (By.CSS_SELECTOR, data_testid('signal-row-symbol'))
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

    def get_last_symbol(self, section: MarketsSection = None, store_data: DotDict = None):
        """Get lastest symbol of section: My Trade, Top Picks, Top Gainer"""
        # Handle signal, sometimes the items do not show

        if section:
            if MarketsSection.SIGNAL in list(section):
                retries = 3
                signal_displayed = self.actions.is_element_displayed(self.__signal_symbol, timeout=5)
                while not signal_displayed and retries:
                    logger.debug("- Retries loading signals")
                    self.refresh_page()
                    self.wait_for_spin_loader()
                    signal_displayed = self.actions.is_element_displayed(self.__signal_symbol)
                    retries += -1

            locator_map = {
                MarketsSection.MY_TRADE: self.__my_trade_symbol,
                MarketsSection.TOP_PICKS: self.__top_picks_symbol,
                MarketsSection.TOP_GAINER: self.__top_gainer_symbol,
                MarketsSection.SIGNAL: self.__signal_symbol
            }

            for _section in section:
                symbol = self.actions.get_text(locator_map[_section])
                if store_data is not None:
                    store_data |= {_section: symbol}

            return symbol

        res = {
            MarketsSection.MY_TRADE: self.actions.get_text(self.__my_trade_symbol),
            MarketsSection.TOP_PICKS: self.actions.get_text(self.__top_picks_symbol),
            MarketsSection.TOP_GAINER: self.actions.get_text(self.__top_gainer_symbol),
            MarketsSection.SIGNAL: self.actions.get_text(self.__signal_symbol)
        }

        if store_data is not None:
            store_data |= res

        return res

    def click_arrow_icon(self, arrow: MarketsSection):
        self.actions.click(cook_element(self.__redirect_arrow, arrow))

    def select_symbol(self, section: MarketsSection | str):
        match section:
            case MarketsSection.MY_TRADE:
                locator = self.__my_trade_symbol

            case MarketsSection.TOP_PICKS:
                locator = self.__top_picks_symbol

            case MarketsSection.TOP_GAINER:
                locator = self.__top_gainer_symbol

            case MarketsSection.SIGNAL:
                locator = self.__signal_symbol

            case _:
                raise ValueError("Invalid Markets Section !!")
        self.actions.click(locator)

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
    def verify_my_trade_last_item(self, symbol: str, trade_type: TradeType):
        logger.debug(f"- Check last item is: {symbol!r}")
        actual_symbol = self.actions.get_text(self.__my_trade_symbol)
        soft_assert(actual_symbol, symbol)

        logger.debug(f"- Check trade_type is: {trade_type!r}")
        actual_type = self.actions.get_text(self.__my_trade_order_type)
        soft_assert(actual_type, trade_type)


    def verify_my_trade_items_list(self, symbols: str | list):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        current_list = self.actions.find_elements(self.__my_trade_symbol)
        current_list = [ele.text.strip() for ele in current_list]

        soft_assert(current_list, symbols)
