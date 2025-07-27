from src.data.objects.trade_obj import ObjTrade
from src.core.actions.mobile_actions import MobileActions
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.trading_modals import TradingModals
from src.page_object.android.components.trade.asset_tab import AssetTab
from src.page_object.android.components.trade.chart import Chart
from src.page_object.android.components.trade.place_order_panel import PlaceOrderPanel
from src.page_object.android.components.trade.watch_list import WatchList
from src.utils.logging_utils import logger
from src.apis.api_client import APIClient
from src.utils.assert_utils import soft_assert, compare_dict


class TradeScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)
        self.asset_tab = AssetTab(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.chart = Chart(actions)
        self.modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
    @staticmethod
    def verify_placed_order_data(trade_object: ObjTrade, api_data: dict):
        """Verify placed order against API data"""

        def _get_api_data():
            logger.info("- Fetching order details from API")
            return APIClient().order.get_orders_details(symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type)

        def _prepare_expected(_api_data: dict, _keys_to_check: list) -> dict:
            _expected = {k: v for k, v in _api_data.items() if k in _keys_to_check}
            # Round floats for comparison
            for key in _expected:
                if isinstance(_expected[key], float):
                    _expected[key] = round(_expected[key], ndigits=ObjTrade.DECIMAL)
            _expected["volume"] = _api_data.get("lotSize")
            return _expected

        if not api_data:
            logger.warning("- Initial API data is empty, retrying...")
            api_data = _get_api_data()

        if not api_data:
            soft_assert(False, True, error_message="API order data is empty!")
            return

        # Prepare actual and expected data
        actual = trade_object.api_data_format()
        keys_to_check = list(actual.keys())
        expected = _prepare_expected(api_data, keys_to_check)

        # Compare with tolerance
        logger.debug("- Comparing actual vs expected with tolerance")
        result = compare_dict(
            actual,
            expected,
            tolerance_percent=0.1,
            tolerance_fields=trade_object.tolerance_fields(api_format=True) + ["openPrice"]
        )["res"]

        if not result:
            logger.warning("- Mismatch detected, retrying API fetch and rechecking")
            api_data = _get_api_data()
            expected = _prepare_expected(api_data, keys_to_check)

        # Final soft assert
        soft_assert(
            actual,
            expected,
            tolerance=0.1,
            tolerance_fields=trade_object.tolerance_fields(api_format=True) + ["openPrice"]
        )
