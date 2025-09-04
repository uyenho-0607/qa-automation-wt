from src.apis.api_base import BaseAPI
from src.data.enums import AssetTabs
from src.utils.format_utils import format_dict_to_string
from src.utils.logging_utils import logger


class UserAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    _oct_endpoint = "/user/v1/preference"
    _hide_order_endpoint = "/user/v1/order/hide/preference"
    _user_account = "/user/v1/account"

    def patch_oct(self, enable=True):
        payload = {
            "category": "ONE_CLICK_TRADING",
            "type": "OCT_ENABLE",
            "value": "true" if enable else "false"
        }
        logger.debug(f"[API] Set ONE_CLICK_TRADING (enable:{enable!r})")
        resp = self.patch(self._oct_endpoint, payload)
        return resp

    def patch_show_all(self, asset_tab=AssetTabs.OPEN_POSITION):
        payload = {
            "orderType": asset_tab.name,
            "hiddenColumnList": []
        }
        logger.debug(f"[API] Show all column preferences (tab:{asset_tab.value})")
        resp = self.patch(self._hide_order_endpoint, payload)
        return resp

    def get_user_account(self, get_acc=True):
        logger.debug("[API] Get user account")
        resp = self.get(endpoint=self._user_account, fields_to_show=["tradingAccounts"])

        if get_acc:
            account = resp["tradingAccounts"][0]

            extract_acc = {
                "id": account["metatraderId"],
                "name": account["accountName"],
                "type": account["accountType"],
                "currency": account["baseCurrency"],
                "leverage": account["leverage"]
            }

            return extract_acc

        return resp
