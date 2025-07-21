import random
from typing import List

from src.data.enums import BaseEnum, OrderType
from src.data.project_info import ProjectConfig


class AccInfo(BaseEnum):
    BALANCE = "Available Balance"
    DEPOSIT = "Deposit"
    REALISED_PROFIT_LOSS = "Realised Profit/Loss"
    WITHDRAWAL = "Withdrawal"
    CREDIT = "Credit"


class AssetTabs(BaseEnum):
    """Enum representing different asset view tabs and their corresponding table types."""
    OPEN_POSITION = "Open Positions"
    PENDING_ORDER = "Pending Orders"
    HISTORY = "History"
    POSITIONS_HISTORY = "Positions History"
    ORDER_AND_DEALS = "Order and Deals"

    def is_sub_history(self):
        return self in [self.POSITIONS_HISTORY, self.ORDER_AND_DEALS]

    def get_col(self) -> str:
        """Get the corresponding table value for the tab."""
        table_mapping = {
            self.OPEN_POSITION: "open",
            self.PENDING_ORDER: "pending",
            self.HISTORY: "history",
            self.POSITIONS_HISTORY: "history-position",
            self.ORDER_AND_DEALS: "order-and-deals"
        }

        return table_mapping.get(self, self)

    @classmethod
    def get_tab(cls, order_type: OrderType | str):
        return cls.OPEN_POSITION if order_type == OrderType.MARKET else cls.PENDING_ORDER


class SortOptions(BaseEnum):
    """Enum representing sorting options for different asset views."""
    OPEN_DATE = "Open Date"
    SYMBOL = "Symbol"
    CLOSE_DATE = "Close Date"
    PROFIT = "Profit"

    @classmethod
    def position_history(cls) -> List[str]:
        """Get sort options for position history view."""
        return [cls.OPEN_DATE, cls.SYMBOL, cls.CLOSE_DATE, cls.PROFIT]

    @classmethod
    def open_positions(cls) -> List[str]:
        """Get sort options for open positions view."""
        return [cls.OPEN_DATE, cls.SYMBOL, cls.PROFIT]

    @classmethod
    def pending_orders(cls) -> List[str]:
        """Get sort options for pending orders view."""
        return [cls.OPEN_DATE, cls.SYMBOL]


class BulkCloseOpts(BaseEnum):
    """Enum representing bulk close operation options."""
    ALL = "all"
    PROFIT = "profit"
    LOSS = "loss"


class ColPreference(BaseEnum):
    """Enum representing available columns for asset tables."""
    SHOW_ALL = "Show all"
    UNITS = "Units"
    PROFIT = "Profit"
    OPEN_DATE = "Open Date"
    CLOSE_DATE = "Close Date"
    SYMBOL = "Symbol"
    ENTRY_PRICE = "Entry Price"
    PRICE = "Price"
    CLOSE_PRICE = "Close Price"
    CURRENT_PRICE = "Current Price"
    TAKE_PROFIT = "Take Profit"
    STOP_LOSS = "Stop Loss"
    FILL_POLICY = "Fill Policy"
    EXPIRY = "Expiry"
    EXPIRY_DATE = "Expiry Date"
    STOP_LIMIT_PRICE = "Stop Limit Price"
    SWAP = "Swap"
    COMMISSION = "Commission"
    REMARKS = "Remarks"

    @classmethod
    def __get_volume_label(cls) -> str:
        """Get the appropriate volume label based on server type."""
        return "Size" if not ProjectConfig.is_non_oms() else "Volume"

    @classmethod
    def get_display_headers(cls, tab: AssetTabs, asset_page=False) -> List[str]:
        """
        Get the display headers for a specific asset tab.
        Args:
            tab: The asset tab to get headers for
            asset_page: checking headers in asset page
        Returns:
            List of column headers appropriate for the tab
        """
        volume_label = cls.__get_volume_label()
        base_headers = ["Order No.", "Type"] + (["Symbol"] if asset_page else [])

        display_headers = {
            AssetTabs.OPEN_POSITION: [
                                         cls.OPEN_DATE, cls.PROFIT, cls.UNITS, cls.ENTRY_PRICE,
                                         cls.CURRENT_PRICE, cls.TAKE_PROFIT, cls.STOP_LOSS,
                                         cls.SWAP, cls.COMMISSION, volume_label
                                     ] + base_headers,

            AssetTabs.PENDING_ORDER: [
                                         cls.UNITS, cls.EXPIRY, cls.PRICE, cls.CURRENT_PRICE,
                                         cls.TAKE_PROFIT, cls.STOP_LOSS, volume_label
                                     ] + base_headers + ([
                                                             cls.EXPIRY_DATE, cls.STOP_LIMIT_PRICE, cls.FILL_POLICY
                                                         ] if ProjectConfig.is_non_oms() else []),

            AssetTabs.HISTORY: [
                                   cls.CLOSE_DATE, cls.PROFIT, cls.UNITS, cls.ENTRY_PRICE,
                                   cls.CLOSE_PRICE, cls.TAKE_PROFIT, cls.STOP_LOSS,
                                   cls.SWAP, cls.COMMISSION, cls.REMARKS, volume_label
                               ] + base_headers + ["Status"]
        }

        return display_headers[tab]

    @classmethod
    def get_random_columns(cls, tab: AssetTabs, amount: int = 1) -> List[str]:
        """
        Get random column preferences for a specific asset tab.
        Args:
            tab: The asset tab to get columns for
            amount: Number of random columns to return
        Returns:
            List of random column names
        """
        if tab == AssetTabs.OPEN_POSITION:
            available_cols = [cls.UNITS, cls.ENTRY_PRICE, cls.CURRENT_PRICE,
                              cls.TAKE_PROFIT, cls.STOP_LOSS, cls.SWAP]
        elif tab == AssetTabs.PENDING_ORDER:
            available_cols = [cls.UNITS, cls.EXPIRY, cls.PRICE, cls.CURRENT_PRICE,
                              cls.TAKE_PROFIT, cls.STOP_LOSS]
            if ProjectConfig.is_non_oms():
                available_cols.extend([cls.EXPIRY_DATE, cls.STOP_LIMIT_PRICE, cls.FILL_POLICY])
        else:  # History
            available_cols = [cls.UNITS, cls.ENTRY_PRICE, cls.CLOSE_PRICE,
                              cls.TAKE_PROFIT, cls.STOP_LOSS, cls.SWAP,
                              cls.COMMISSION, cls.REMARKS]

        return random.sample(available_cols, k=min(amount, len(available_cols)))
