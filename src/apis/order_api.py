from src.apis.api_base import BaseAPI
from src.data.enums import AssetTabs, OrderType
from src.utils.logging_utils import logger


class OrderAPI(BaseAPI):
    _counts_endpoint = "/order/v1/counts"
    _pending_endpoint = "/order/v1/pending"
    _open_endpoint = "/order/v2"

    def __init__(self):
        super().__init__()

    def get_counts(self, symbol: str = "", order_type: OrderType = OrderType.MARKET):
        """
        Get current order counts of open positions or pending orders
        :param symbol: specific symbol, if not provided, GET all
        :param order_type: return open orders if order type is Market, else >> pending
        :return: Return market/ pending orders count for a specific symbol/ all symbols
        """
        logger.debug(f"[API] Get order amount (order_type:{order_type.value})")
        resp = self.get(endpoint=self._counts_endpoint, params={"symbol": symbol} if symbol else {})
        key = "market" if order_type == OrderType.MARKET else "pending"

        return resp.get(f"{key}OrderCounts")

    def get_orders_details(
            self,
            symbol: str = None,
            order_type: OrderType = OrderType.MARKET,
            order_id: int | str = None
    ):
        """
        Get order details of open positions or pending orders
        :param symbol: specific symbol
        :param order_type: order type (Market, Limit, Stop, StopLimit)
        :param order_id: specific order id, if provided, return order details by this order_id
        :return: Return all orders details for a specific symbol, or order details by order_id
        """
        tab = AssetTabs.get_tab(order_type)

        endpoint = self._pending_endpoint if tab == AssetTabs.PENDING_ORDER else self._open_endpoint

        logger.info(f"[API] Get order details ({'All' if not symbol else f'symbol:{symbol}'})")
        resp = self.get(endpoint, {"symbol": symbol})

        if order_id:
            # return order details by order_id
            resp = next((item for item in resp if item.get("orderId") == order_id), None)

        return resp

    def get_order_id_list(self, symbol: str, order_type: OrderType = OrderType.MARKET):
        """
        Get order id list of open positions or pending orders
        :param symbol: specific symbol
        :param order_type: order type (Market, Limit, Stop, StopLimit)
        :return: Return order id list for a specific symbol
        """
        resp = self.get_orders_details(symbol, order_type)
        order_ids = [item.get("orderId") for item in resp]
        return order_ids
