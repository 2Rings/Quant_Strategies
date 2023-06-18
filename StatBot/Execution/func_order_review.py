from func_position_calls import (
    query_existing_order,
    get_open_position,
    get_active_order,
)
from func_calculation import get_trade_details
from config_ws_connect import ws_public

# Check order items


def check_order(ticker, order_id, remaining_capital, direction="Long"):
    # Get current order book

    orderbook = ws_public.fetch(f"orderBookL2_25.{ticker}")

    # Get latest price
    order_price, _, _ = get_trade_details(orderbook)

    # Get trade details
    order_price, order_qauntity, order_status = query_existing_order(
        ticker, order_id, direction
    )

    # Get open Position

    position_price, position_quantity = get_open_position(ticker, direction)

    # Get active position
    active_order_price, active_order_quantity = get_active_order(ticker)

    # Determine action - trade complete - stop placing orders
    if position_quantity >= remaining_capital and position_quantity > 0:
        return "Trade Complete"

    # Determine action - position filled - buy more
    if order_status == "Filled":
        return "Position Filled"

    # Determine action - order active - do nothing
    active_items = ["Created", "New"]
    if order_status in active_items:
        return "Order Active"

    # Determine action - partial filled order - do nothing
    if order_status == "PartiallyFilled":
        return "Partial Fill"

    # Determine action - order failed - try place order again
    cancel_items = ["Cancelled", "Rejected", "PendingCancel"]
    if order_status in cancel_items:
        return "Try Again"
