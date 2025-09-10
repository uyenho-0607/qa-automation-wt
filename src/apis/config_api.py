from src.apis.api_base import BaseAPI


class ConfigAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    _endpoint = "/config/v1/company/user"

    def get_product_subscription(self) -> str:
        """
        Calls the API and returns the product subscription as a single string, e.g. "PREMIUM".
        Assumes there is always exactly one subscription.
        """
        resp = self.get(endpoint=self._endpoint)

        prod_list_info = resp["productSubscriptionList"]
        subscription = prod_list_info[0]["productSubscription"]  # take the first item

        return subscription
