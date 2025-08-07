from src.core.actions.mobile_actions import MobileActions
from src.page_object.android.base_screen import BaseScreen


class NewsScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
