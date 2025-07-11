from src.data.enums import OrderType
from src.data.objects.base_object import BaseObject
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.data.ui_messages import UIMessages
from src.utils.format_utils import format_prices, remove_commas, add_commas


class ObjectNoti(BaseObject):
    """A class representing a notification with trade information.
    Attributes:
    - trade_object: DotDict (should be loaded from ObjectTrade)
    """

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

    @staticmethod
    def __format_volume(message: str) -> str:
        """Format volume text based on server type."""
        if ProjectConfig.is_mt4():
            return message.replace("Volume", "Size")

        return message

    def __format_prices(self):
        self.stop_loss, self.take_profit, self.entry_price = format_prices([self.stop_loss, self.take_profit, self.entry_price], ObjectTrade.DECIMAL)

    def order_submitted_banner(self, **kwargs):
        """Get order submitted banner message."""
        self._update_attributes(**kwargs)
        # banner title
        title = UIMessages.ORDER_SUBMITTED_BANNER_TITLE.format(self.order_type.title())
        # banner des
        self.__format_prices()
        order_type = self.trade_type + (f" {self.order_type.upper()}" if self.order_type != OrderType.MARKET else "")
        des = UIMessages.ORDER_PLACED_BANNER_DES.format(self.symbol, order_type, self.volume, self.units)

        if self.stop_limit_price:
            des += f" Stop Limit Price: {self.stop_limit_price}."

        if self.entry_price and not self.order_type == OrderType.MARKET:
            des += f" Price: {self.entry_price}."

        if self.stop_loss and self.stop_loss != "--":
            des += f" Stop Loss: {self.stop_loss}."

        if self.take_profit and self.take_profit != "--":
            des += f" Take Profit: {self.take_profit}."

        return self.__format_volume(title), self.__format_volume(des)

    def order_updated_banner(self, **kwargs):
        """Get order updated banner message."""
        self._update_attributes(**kwargs)
        title = UIMessages.ORDER_UPDATED_BANNER_TITLE.format(self.order_type.title())

        # handle description
        trade_type = f"{self.trade_type.upper()} {self.order_type.upper()}" if not self.order_type == OrderType.MARKET else self.trade_type.upper()
        self.__format_prices()
        des = UIMessages.ORDER_UPDATED_BANNER_DES.format(self.symbol, trade_type, self.volume, self.units)

        if self.trade_object.get("stop_limit_price"):
            des += f" Stop Limit Price: {self.stop_limit_price}."

        des += f" Entry Price: {self.entry_price}."

        if self.stop_loss and self.stop_loss != "--":
            des += f" Stop Loss: {self.stop_loss}."

        if self.take_profit and self.take_profit != "--":
            des += f" Take Profit: {self.take_profit}."

        if not self.order_type == OrderType.MARKET:
            des = des.replace("Entry Price", "Price")

        return self.__format_volume(title), self.__format_volume(des)

    def open_position_details(self, order_id, remove_price=False, **kwargs):
        """Get open position notification message."""
        self._update_attributes(**kwargs)
        self.__format_prices()

        message = UIMessages.OPEN_POSITION_NOTI_RESULT.format(
            order_id, self.symbol, self.volume, self.units, add_commas(remove_commas(self.entry_price, to_float=True))
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
        # Position Closed: #8160987 DASHUSD.std: Size 42 / Units 420 @ 22.77, Loss of -680.4
        # skip checking price as for some symbols, it changes a lot
        message = UIMessages.POSITION_CLOSED_NOTI_RESULT.split(",")[0].format(
            self.order_id, self.symbol, self.volume, self.units,
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
