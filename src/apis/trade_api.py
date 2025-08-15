import random
from datetime import datetime, timedelta

from src.apis.api_base import BaseAPI
from src.apis.market_api import MarketAPI
from src.apis.order_api import OrderAPI
from src.data.enums import Expiry, TradeType, OrderType, SLTPType, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.utils import DotDict
from src.utils.format_utils import format_with_decimal
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_trading_params


class TradeAPI(BaseAPI):
    """API client for placing trading orders"""

    _endpoint = "/trade/v2/"
    _bulk_open_order = "/trade/v1/bulk"
    _bulk_pending_order = "/trade/v1/limit/bulk"

    _symbol_details = DotDict()

    def __init__(self):
        super().__init__()
        self._order_api = OrderAPI()
        self._market_api = MarketAPI()

    def _get_symbol_details(self, symbol) -> DotDict:
        """Get and cache symbol details for calculating trade parameters."""
        if symbol not in self._symbol_details:
            logger.debug(f"Getting symbol details for {symbol!r}")
            resp = self._market_api.get_symbol_details(symbol=symbol)

            self._symbol_details[symbol] = DotDict({
                "point_step": resp["pointStep"],
                "contract_size": resp["contractSize"],
                "current_price": {
                    TradeType.BUY: float(format_with_decimal(resp["ask"], resp["pointStep"])),
                    TradeType.SELL: float(format_with_decimal(resp["bid"], resp["pointStep"]))
                }
            })

        return self._symbol_details[symbol]

    @staticmethod
    def _get_order_type_code(order_type: OrderType, trade_type: TradeType) -> int:
        """Get the order type code for the API."""
        return ObjTrade.get_order_type_map(order_type, trade_type)

    @staticmethod
    def _get_expiration_timestamp(expiry, move_days: int = 1) -> int | None:
        """Get expiration timestamp for tomorrow at 21:00:00."""
        if expiry not in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
            return None

        now = datetime.now()
        tomorrow_9pm = now.replace(hour=21, minute=0, second=0, microsecond=0) + timedelta(days=move_days)
        return int(tomorrow_9pm.timestamp() * 1000)

    def _build_payload(self, trade_object: ObjTrade) -> dict:
        """Build the API payload for placing an order."""
        symbol = trade_object.symbol
        trade_type = trade_object.trade_type
        order_type = trade_object.order_type

        # Get symbol details and current price
        symbol_details = self._get_symbol_details(symbol)
        current_price = symbol_details.current_price[trade_type]

        # Calculate trade parameters
        indicate = trade_object.get("indicate", SLTPType.PRICE)
        trade_params = calculate_trading_params(current_price, trade_type, order_type, sl_type=indicate.lower(),
                                                tp_type=indicate.lower())

        # Build base payload
        payload = {
            "orderType": self._get_order_type_code(order_type, trade_type),
            "symbol": symbol,
            "lotSize": random.randint(10, 20),
            "indicate": indicate.upper(),
            "stopLoss": float(trade_params.stop_loss),
            "takeProfit": float(trade_params.take_profit),
            "fillPolicy": ObjTrade.get_fill_policy_map(trade_object.get("fill_policy")),
            "tradeExpiry": ObjTrade.get_expiry_map(trade_object.get("expiry")),
            "price": float(trade_params.entry_price) if not order_type.is_market() else None,
            "priceTrigger": float(trade_params.stop_limit_price) if order_type.is_stp_limit() else None,
            "expiration": self._get_expiration_timestamp(trade_object.get("expiry"))
        }

        if trade_object.get("stop_loss", None) == 0:
            payload["stopLoss"] = None

        if trade_object.get("take_profit", None) == 0:
            payload["takeProfit"] = None

        # Remove None values
        return {k: v for k, v in payload.items() if v is not None}

    def _update_trade_object(self, trade_object: DotDict, payload: dict, response: dict, update_price=True):
        """Update trade object with response data and calculated values."""
        symbol_details = self._symbol_details[trade_object.symbol]

        # Update with response data
        payload["order_id"] = response["clOrdId"]

        # Calculate units and volume
        payload["units"] = symbol_details.contract_size * payload["lotSize"]
        payload["volume"] = payload.pop("lotSize")
        payload["entry_price"] = str(payload.pop("price", 0))

        # Handle stop limit price
        if "priceTrigger" in payload:
            payload["stop_limit_price"] = payload.pop("priceTrigger")

        # Set default SL/TP values
        payload["stop_loss"] = payload.pop("stopLoss", "--")
        payload["take_profit"] = payload.pop("takeProfit", "--")

        # For market orders, get actual entry price from order details
        if trade_object.order_type == OrderType.MARKET and update_price:
            logger.debug("Getting placed order details for updating entry_price")
            order_details = self._order_api.get_orders_details(
                trade_object.symbol, trade_object.order_type, payload["order_id"]
            )

            # Update entry price with actual executed price
            payload["entry_price"] = round(order_details["openPrice"], ndigits=ObjTrade.DECIMAL)

            # Update SL/TP if using points
            if payload.pop("indicate", "").lower() == SLTPType.POINTS.lower():
                payload["stop_loss"] = format_with_decimal(
                    order_details.get("stopLoss") or "--", symbol_details.point_step
                )
                payload["take_profit"] = format_with_decimal(
                    order_details.get("takeProfit") or "--", symbol_details.point_step
                )

        # Update the trade object
        trade_object.update(payload)
        trade_object.pop("indicate", None)

    def post_order(self, trade_object: ObjTrade, update_price=True):
        """Place a trading order."""
        max_retries = 3

        # Determine endpoint
        order_type = OrderType.MARKET if trade_object.order_type == OrderType.MARKET else OrderType.LIMIT
        endpoint = f"{self._endpoint}{order_type.lower()}"

        for attempt in range(max_retries):
            try:
                # Build fresh payload for each attempt (in case price calculations were invalid)
                payload = self._build_payload(trade_object)

                # Make the API call (server errors are handled by @after_request decorator)
                response = self.post(endpoint, payload)

                # Update trade object with response data
                self._update_trade_object(trade_object, payload, response, update_price)

                return response

            except Exception as e:
                # Check if it's a client error (4xx) that might be due to invalid payload
                logger.warning(f"Client error on attempt {attempt + 1}/{max_retries}: {str(e)}")

                if attempt < max_retries - 1:
                    logger.debug(f"Retrying with fresh payload...")
                    continue
                else:
                    logger.error(f"Failed after {max_retries} attempts with fresh payloads")
                    raise
        return None

    def bulk_close_orders(self, orders, tab: AssetTabs):
        """
        Bulk close multiple orders in one API call

        :param orders: List of dicts with orderId, symbol, lotSize, fillPolicy
        :param tab: Asset tab type from AssetTabs enum
        :return: API response
        """
        endpoint = self._bulk_open_order if tab == AssetTabs.OPEN_POSITION else self._bulk_pending_order
        return self.put(endpoint, orders)

