import random
from typing import Any

from src.data.enums import TradeType, OrderType
from src.data.enums.trading import SLTPType
from src.data.objects.trade_object import ObjectTrade
from src.utils import DotDict
from src.utils.format_utils import format_with_decimal, format_str_price
from src.utils.format_utils import remove_comma


def count_leading_zeros_after_decimal(number):
    # Convert to string in case of scientific notation
    num_str = f"{number:.50f}".rstrip('0')  # long precision, remove trailing 0s
    if '.' not in num_str:
        return 0

    decimal_part = num_str.split('.')[1]
    count = 0
    for ch in decimal_part:
        if ch == '0':
            count += 1
        else:
            break
    return count


def _random_min_point_distance(live_price: str | float) -> int:
    """
    Calculate random point distance based on live price.
    Ensures the adjusted price will be valid for the given price level.
    Args:
        live_price: Current market price
    """
    live_price = remove_comma(live_price)
    # Get the decimal precision to calculate valid range
    one_point = _get_decimal_precision(live_price)
    if int(float(live_price)) >= 1:
        max_point = int(float(live_price)) / one_point

    else:
        zero_count = count_leading_zeros_after_decimal(live_price)
        max_point = 1 / (one_point * 10 * int(f'1{'0' * zero_count}'))
    res = random.randint(int(max_point * 0.6), int(max_point * 0.95))

    return res


def _get_decimal_precision(number_str: str | float) -> float:
    """
    Extract the decimal precision from a number string. Input number string (e.g. "62.802", "62.80", "62.8") -> Output decimal precision (e.g. 0.001, 0.01, 0.1)
    """
    number_str = str(number_str)
    if '.' not in number_str:
        return 1.0

    decimal_part = number_str.split('.')[1]
    return 1.0 / (10 ** len(decimal_part))


def _get_price_adjustment(live_price: str | float, is_invalid=False):
    """
    Get the price adjustment: add and subtract a random value from live price
    live_price: str | float, input live price - in case order_type:
        - MARKET: live_price
        - LIMIT: entry_price
        - STOP: entry_price
        - STOP_LIMIT: stop_limit_price
    is_invalid: bool, if True, return invalid price adjustment
    """

    one_point_value = _get_decimal_precision(live_price)
    price_adjustment = one_point_value * _random_min_point_distance(live_price)
    live_price = remove_comma(live_price)

    if is_invalid:
        price_adjustment = -price_adjustment

    increased_price = abs(live_price + price_adjustment)
    decreased_price = abs(live_price - price_adjustment)

    increased_price = format_with_decimal(increased_price, ObjectTrade.DECIMAL or one_point_value)
    decreased_price = format_with_decimal(decreased_price, ObjectTrade.DECIMAL or one_point_value)

    return increased_price, decreased_price


def calculate_sl_tp_price(
        live_price: str | float,
        trade_type: TradeType = TradeType.BUY,
        invalid: bool = False,
) -> DotDict:
    """
    Calculate stop loss and take profit price based on live price.
    Logic: stop loss less than live price, take profit greater than live price. Vice versa for SELL.
    Args:
        live_price (float):
            - MARKET: live_price
            - LIMIT: price
            - STOP: price
            - STOP_LIMIT: stop_limit_price
        trade_type (TradeType): Type of order (BUY or SELL)
        invalid (bool): Whether to reverse the calculation
    Returns:
        tuple[float, float]: stop loss and take profit price
    """
    increased_price, decreased_price = _get_price_adjustment(live_price, invalid)
    res = {
        TradeType.BUY: DotDict(stop_loss=decreased_price, take_profit=increased_price),
        TradeType.SELL: DotDict(stop_loss=increased_price, take_profit=decreased_price)
    }

    return res[trade_type]


def _random_sl_tp_points(
        live_price: str | float,
        trade_type: TradeType = TradeType.BUY,
) -> DotDict:
    """
    Generate random stop loss and take profit points based on trade type.
    BUY:
        SL = Entry - (points * one_point_value) -> must cap to avoid negative
        TP = Entry + (points * one_point_value) -> always safe
    SELL:
        SL = Entry + (points * one_point_value) -> always safe
        TP = Entry - (points * one_point_value) -> must cap to avoid negative
    """
    one_point_value = _get_decimal_precision(live_price)
    live_price = remove_comma(live_price)
    max_safe_points = round((live_price / one_point_value) * 0.9)

    def get_points(is_limited: bool) -> int:
        min_points = round(max_safe_points * 0.5)
        if is_limited:
            return random.randint(min_points, max_safe_points)

        return random.randint(min_points, max_safe_points * 2)

    # For BUY: SL is limited, TP is unlimited
    # For SELL: SL is unlimited, TP is limited
    is_buy = trade_type == TradeType.BUY
    sl_points = get_points(is_buy)
    tp_points = get_points(not is_buy)

    return DotDict(stop_loss=sl_points, take_profit=tp_points)


def calculate_price(
        live_price: str | float,
        trade_type: TradeType = TradeType.BUY,
        order_type: OrderType = OrderType.LIMIT,
        invalid: bool = False,
) -> str:
    """
    Calculate entry price based on live price.
    Logic:
    - BUY: in case order_type:
        - MARKET: entry_price = current_price
        - LIMIT: price less than live_price -> price = live_price - price_adjustment
        - STOP: price greater than live_price ->  = live_price + price_adjustment
        - STOP_LIMIT: price = stop_limit_price + price_adjustment (live_price should input as stop_limit_price)

    - SELL: vice versa
    """
    increased_price, decreased_price = _get_price_adjustment(live_price, invalid)
    res = {
        TradeType.BUY: {
            OrderType.LIMIT: decreased_price,
            OrderType.STOP: increased_price,
            OrderType.STOP_LIMIT: increased_price
        },
        TradeType.SELL: {
            OrderType.LIMIT: increased_price,
            OrderType.STOP: decreased_price,
            OrderType.STOP_LIMIT: decreased_price
        }
    }

    return res[trade_type].get(order_type, live_price)


def calculate_stp_price(
        price: str | float,
        trade_type: TradeType = TradeType.BUY,
        invalid: bool = False,
) -> str:
    """
    Calculate stop limit price based on price.
    Logic:
    - BUY: stop_limit_price = price + price_adjustment
    - SELL: vice versa
    """
    # increased_price, decreased_price = _get_price_adjustment(price, invalid)
    # return increased_price if trade_type == TradeType.BUY else decreased_price
    return calculate_price(price, trade_type, OrderType.STOP_LIMIT, invalid)


def _calculate_trade_price(
        live_price: str | float,
        trade_type: TradeType = TradeType.BUY,
        order_type: OrderType = OrderType.MARKET,
        invalid: bool = False,
) -> DotDict[Any, Any]:
    """
    Calculate trade parameters based on current price, trade type, order type, invalid flag, and modification flag.
    """
    res = DotDict()

    # Stop Limit Price:
    valid_stp, invalid_stp = None, None

    # Update value for stop limit price if order_type == STOP LIMIT
    if order_type.is_stp_limit():
        valid_stp = calculate_stp_price(live_price, trade_type)
        invalid_stp = calculate_stp_price(live_price, trade_type, invalid=True)

    # Price, in case order_type = MARKET >> price = entry_price = live price
    # if stp_limit: price > stp_limit (BUY), < stp_limit (SELL)
    valid_price = calculate_price(valid_stp or live_price, trade_type, order_type)
    invalid_price = calculate_price(valid_stp or live_price, trade_type, order_type, invalid=True)

    # stop_loss and take profit
    stop_loss, take_profit = calculate_sl_tp_price(
        valid_stp if order_type.is_stp_limit() else valid_price, trade_type, invalid=invalid
    ).values()

    # Update result dict:
    res["entry_price"] = invalid_price if invalid else valid_price
    res["stop_limit_price"] = invalid_stp if invalid else valid_stp
    res["stop_loss"] = stop_loss
    res["take_profit"] = take_profit

    return res


def calculate_trade_parameters(
        live_price: str | float,
        trade_type: TradeType = TradeType.BUY,
        order_type: OrderType = OrderType.MARKET,
        sl_type: SLTPType | str = SLTPType.PRICE,
        tp_type: SLTPType | str = SLTPType.PRICE,
        invalid: bool = False,
) -> DotDict[Any, Any]:
    """
    Calculate trade parameters based on current price, trade type, order type, invalid flag, sl_type, tp_type.
    """
    prices = _calculate_trade_price(live_price, trade_type, order_type, invalid)
    sl_tp_points = _random_sl_tp_points(
        prices.stop_limit_price if order_type.is_stp_limit() else prices.entry_price, trade_type
    )

    return DotDict(
        entry_price=prices.entry_price,
        stop_limit_price=prices.stop_limit_price,
        stop_loss=(prices if sl_type == SLTPType.PRICE else sl_tp_points).stop_loss,
        take_profit=(prices if tp_type == SLTPType.PRICE else sl_tp_points).take_profit,
    )


def calculate_sl_tp(live_price, trade_type, sl_type, tp_type):
    """
    Calculate updated stop loss and take profit based on live price, keeping other prices unchanged.
    Args:
        live_price: Current market price to base SL/TP calculations on
        trade_type: TradeType (BUY or SELL)
        sl_type: SLTPType (PRICE or POINTS) - determines if SL should be price or points
        tp_type: SLTPType (PRICE or POINTS) - determines if TP should be price or points
    Returns:
        DotDict with stop_loss and take_profit only
    """
    # Calculate SL/TP prices based on live price
    sl_tp_prices = calculate_sl_tp_price(live_price, trade_type)
    
    # Calculate SL/TP points based on live price
    sl_tp_points = _random_sl_tp_points(live_price, trade_type)
    
    return DotDict(
        stop_loss=(sl_tp_prices if sl_type == SLTPType.PRICE else sl_tp_points).stop_loss,
        take_profit=(sl_tp_prices if tp_type == SLTPType.PRICE else sl_tp_points).take_profit,
    )


def calculate_partial_close(trade_object):
    volume, units = int(trade_object.volume), int(remove_comma(trade_object.units))
    close_volume = random.randint(1, volume - 1)
    left_volume = volume - close_volume
    left_units = int(units * left_volume / volume)
    close_units = int(units - left_units)

    return DotDict(
        left_volume=format_str_price(left_volume, 0),
        close_volume=format_str_price(close_volume, 0),
        left_units=format_str_price(left_units, 0),
        close_units=format_str_price(close_units, 0),
    )
