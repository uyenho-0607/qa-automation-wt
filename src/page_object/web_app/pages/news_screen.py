from src.core.actions.web_actions import WebActions
from src.page_object.web_app.base_page import BasePage


class NewsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
