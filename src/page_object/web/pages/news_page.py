from src.core.actions.web_actions import WebActions
from src.data.enums import URLPaths
from src.page_object.web.base_page import BasePage


class NewsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #

    # ------------------------ ACTIONS ------------------------ #
    def verify_page_url(self):
        super().verify_page_url(URLPaths.NEWS)

    # ------------------------ VERIFY ------------------------ #
