from config_execution_api import session_private, limit_order_basis
from config_ws_connect import ws_public
from func_calculation import get_trade_details

# Set leverage
def set_leverage(ticker):
    
    # Setting the leverage
    levearge_set = session_private.cross_isolated_margin_switch(
        symbol=ticker,
        is_isolated=True,
        buy_leverage=1,
        sell_levearge=2
    )

    return

def place_order(ticker, price, quantity, direction, stop_loss):
    
    side = "Buy" if direction == "Long" else "Sell"
    reduce_only = False

    # Get limit order
    if limit_order_basis:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type = "Limit",
            qty = quantity,
            price = price,
            time_in_force ="PostOnly",
            reduce_only  = reduce_only,
            close_on_trigger=False,
            stop_loss=stop_loss
        )
    else:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type = "Market",
            qty = quantity,
            time_in_force ="GoodTillCancell",
            reduce_only  = reduce_only,
            close_on_trigger=False,
            stop_loss=stop_loss
        )

    return order

# Initialize execution
def initialize_order_execution(ticker, direction, capital):
    # counts = 0
    # while True:
    orderbook = ws_public.fetch(f"orderBookL2_25{ticker}")
        # if orderbook and counts == 0:
    if orderbook:
        order_price, stop_loss, quantity = get_trade_details(orderbook, direction, capital)
        if quantity > 0:
            order = place_order(ticker, order_price, quantity, direction, stop_loss)
            # counts += 1
            if "result" in order.keys():
                if "order_id" in order["result"]:
                    return order["result"]["order_id"]

    return 0 