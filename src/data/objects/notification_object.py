from src.data.enums import OrderType
from src.data.objects.base_object import BaseObject
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.data.ui_messages import UIMessages
from src.utils.format_utils import remove_comma, format_str_price

"""
Notification Sample
1. Banner
- XRPUSD.std - BUY ORDER placed, Size: 1 / Units: 1,000. Stop Loss: 2.5649. Take Profit: 2.5895.
- XRPUSD.std - BUY LIMIT ORDER placed, Size: 1 / Units: 1,000. Price: 2.2000. Stop Loss: 2.1877. Take Profit: 2.2123.
- ETH.USD - BUY STOP LIMIT ORDER placed, Volume: 0.1 / Units: 0.1. Stop Limit Price: 2,993.22. Price: 2,994.18. Stop Loss: 2,991.99. Take Profit: 2,994.45.
- ETH.USD - BUY ORDER updated, Volume: 9 / Units: 9. Entry Price: 2,520.70. Stop Loss: 2,994.23. Take Profit: 2,996.69.

2. Details
- Open Position: Open Position: #8526920 AUDNZD.std: Size 0.02 / Units 2,000 @ 1.07698 
- Position Closed: #7592152 DASHUSD.std: Size 0.02 / Units 0.2 @ 19.92, Loss of -1.82
"""


class ObjectNoti(BaseObject):
    """A class representing a notification with trade information."""

    def __init__(self, trade_object: ObjectTrade):
        super().__init__()
        self.trade_object = trade_object

        self.order_type = trade_object.order_type
        self.trade_type = trade_object.trade_type
        self.symbol = trade_object.symbol
        self.volume = trade_object.volume
        self.units = trade_object.units

        # prices
        self.stop_loss = trade_object.get("stop_loss")
        self.take_profit = trade_object.get("take_profit")
        self.order_id = trade_object.get("order_id", None)
        self.entry_price = trade_object.get("entry_price")
        self.stop_limit_price = trade_object.get("stop_limit_price")

    def __have_sl(self):
        """Check if stop loss having value"""
        return self.stop_loss and self.stop_loss != "--"

    def __have_tp(self):
        return self.take_profit and self.take_profit != "--"

    @staticmethod
    def __format_volume(message: str) -> str:
        """Format volume text based on server type."""
        if ProjectConfig.is_mt4():
            return message.replace("Volume", "Size")

        return message

    @staticmethod
    def __banner_prices(value):
        """Add comma, enough decimal places"""
        return format_str_price(value, ObjectTrade.DECIMAL)

    @staticmethod
    def __detail_prices(value):
        """Only adding comma & remove redundant zero in decimal"""
        value = remove_comma(value)
        return format_str_price(value)

    def __get_order_type(self):
        return self.trade_type + (f" {self.order_type.upper()}" if self.order_type != OrderType.MARKET else "")

    def order_submitted_banner(self, **kwargs):
        """Get order submitted banner title and description."""
        self._update_attributes(**kwargs)
        # banner title
        title = UIMessages.ORDER_SUBMITTED_BANNER_TITLE.format(self.order_type.title())
        # banner des
        des = UIMessages.ORDER_PLACED_BANNER_DES.format(self.symbol, self.__get_order_type(), self.volume, self.units)

        if self.order_type.is_stp_limit():
            des += f" Stop Limit Price: {self.__banner_prices(self.stop_limit_price)}."

        if not self.order_type.is_market():
            des += f" Price: {self.__banner_prices(self.entry_price)}."

        if self.__have_sl():
            des += f" Stop Loss: {self.__banner_prices(self.stop_loss)}."

        if self.__have_tp():
            des += f" Take Profit: {self.__banner_prices(self.take_profit)}."

        return self.__format_volume(title), self.__format_volume(des)

    def order_updated_banner(self, **kwargs):
        """Get order updated banner message."""
        self._update_attributes(**kwargs)
        # banner title
        title = UIMessages.ORDER_UPDATED_BANNER_TITLE.format(self.order_type.title())
        # banner des
        des = UIMessages.ORDER_UPDATED_BANNER_DES.format(self.symbol, self.__get_order_type(), self.volume, self.units)

        if self.order_type.is_stp_limit():
            des += f" Stop Limit Price: {self.__banner_prices(self.stop_limit_price)}."

        des += f" Entry Price: {self.__banner_prices(self.entry_price)}."

        if self.__have_sl():
            des += f" Stop Loss: {self.__banner_prices(self.stop_loss)}."

        if self.__have_tp():
            des += f" Take Profit: {self.__banner_prices(self.take_profit)}."

        if not self.order_type.is_market():
            des = des.replace("Entry Price", "Price")

        return self.__format_volume(title), self.__format_volume(des)

    def open_position_details(self, order_id, remove_price=False, **kwargs):
        """Get open position notification message."""
        self._update_attributes(**kwargs)

        message = UIMessages.OPEN_POSITION_NOTI_RESULT.format(
            order_id, self.symbol, self.volume, self.units, self.__detail_prices(self.entry_price)
        )
        if remove_price:
            message = message.split("@")[0]  # skip checking entry_price as appium is slow and cannot get exact entry value
        return self.__format_volume(message)

    def close_order_success_banner(self, **kwargs):
        self._update_attributes(**kwargs)
        title = UIMessages.CLOSE_ORDER_BANNER_TITLE
        des = UIMessages.CLOSE_ORDER_BANNER_DES.format(self.symbol, self.trade_type.capitalize())
        return title, des

    def position_closed_details(self):
        message = UIMessages.POSITION_CLOSED_NOTI_RESULT.format(
            self.order_id, self.symbol, self.volume, self.units, self.__detail_prices(self.entry_price)
        )
        return self.__format_volume(message)

    @staticmethod
    def bulk_close_open_position_banner(order_ids: list):
        #  Bulk closure of open position
        # Positions #8160917, #8159431, #8159430 and 27 others have been closed.

        title = UIMessages.BULK_CLOSE_OP_BANNER_TITLE

        # des = "Positions #{}, #{}, #{} "
        displayed_order_ids = ", ".join(f"#{str(item)}" for item in order_ids[:3])
        des = f"Positions {displayed_order_ids} "

        other_amount = (len(order_ids) if len(order_ids) <= 30 else 30) - 3 if len(order_ids) > 3 else ''

        des = des.format(*displayed_order_ids)
        if other_amount:
            des += f"and {other_amount} others "

        des += "have been closed."

        return title, des

    def delete_order_banner(self):
        title = UIMessages.DELETE_ORDER_BANNER_TITLE
        des = UIMessages.DELETE_ORDER_BANNER_DES.format(
            self.symbol, f"{self.trade_type.capitalize()} {self.order_type.title()}"
        )
        return title, des

    @staticmethod
    def bulk_delete_order_banner(order_ids: list):
        # Bulk deletion of pending orders
        # Pending orders #8188462, #8188317, #8187221 and 1 others have been deleted.

        title = UIMessages.BULK_DELETE_BANNER_TITLE

        displayed_order_ids = ", ".join(f"#{str(item)}" for item in order_ids[:3])
        des = f"Pending orders {displayed_order_ids} "

        other_amount = (len(order_ids) if len(order_ids) <= 30 else 30) - 3 if len(order_ids) > 3 else ''
        des = des.format(*displayed_order_ids)
        if other_amount:
            des += f"and {other_amount} others "

        des += "have been deleted."
        return title, des
