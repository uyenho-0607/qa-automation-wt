from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.enums import WatchListTab
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.trade.watch_list import WatchList
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class MarketsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (By.XPATH, "//div[contains(text(), '{}')]")
    __horizontal_tab = (By.XPATH, "//div[text()='Favourites']/../..")

    # ------------------------ ACTIONS ------------------------ #

    def select_tab(self, tab: WatchListTab, wait=True):
        """Handle selecting tab for home & markets page"""
        locator = cook_element(self.__tab, tab)

        logger.info(f"- Select tab: {tab.value.capitalize()!r}")
        if self.actions.is_element_displayed(locator):
            self.actions.click(locator)

        else:
            for direction in ["left", "right"]:
                logger.debug(f"- Drag {direction} to show tab")
                self.actions.drag_element_horizontal(self.__horizontal_tab, direction)
                if self.actions.is_element_displayed(locator):
                    self.actions.click(locator)

        not wait or self.wait_for_spin_loader()
    # ------------------------ VERIFY ------------------------ #
