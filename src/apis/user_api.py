from src.apis.api_base import BaseAPI
from src.data.enums import AssetTabs


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
        resp = self.patch(self._oct_endpoint, payload)
        return resp

    def patch_show_all(self, asset_tab=AssetTabs.OPEN_POSITION):
        payload = {
            "orderType": asset_tab.name,
            "hiddenColumnList": []
        }
        resp = self.patch(self._hide_order_endpoint, payload)
        return resp

    def get_user_account(self, get_acc=True):
        resp = self.get(endpoint=self._user_account)
        if get_acc:
            account = resp["tradingAccounts"][0]

            return {
                "id": account["metatraderId"],
                "name": account["accountName"],
                "type": account["accountType"],
                "currency": account["baseCurrency"],
                "leverage": account["leverage"]
            }
        return resp
