from config_execution_api import (
    signal_negative_ticker,
    signal_positive_ticker,
    session_private,
)

# Get position information


def get_position_info(ticker):
    """_summary_

    Args:
        ticker (_type_): _description_

    Returns:
        _type_: _description_
    """
    size = 0
    side = ""

    # Extract position info
    position = session_private.my_position(symbol=ticker)

    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if len(position["result"]) == 2:
                if position["result"][0]["size"] > 0:
                    size = position["result"][0]["size"]
                    side = "Buy"

                else:
                    size = position["result"][1]["size"]
                    side = "Sell"

    # Return output
    return size, side


# Place market close order
def place_market_close_order(ticker, side, size):
    # Close position

    session_private.place_active_order(
        symbol=ticker,
        side=side,
        order_type="Market",
        qty=size,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False,
    )

    return


# Close all positions for both tickers
def close_all_positions(kill_switch):
    # Cancel all active orders

    session_private.cancel_all_active_orders(symbol=signal_positive_ticker)
    session_private.cancel_all_active_orders(symbol=signal_negative_ticker)

    # Get position information
    side_1, size_1 = get_position_info(signal_positive_ticker)
    side_2, size_2 = get_position_info(signal_negative_ticker)

    if size_1 > 0:
        place_market_close_order(signal_positive_ticker, side_2, size_1)  # use Side 2

    if size_2 > 0:
        place_market_close_order(signal_negative_ticker, side_1, size_2)  # use side 1

    # Output results
    kill_switch = 0

    return kill_switch
