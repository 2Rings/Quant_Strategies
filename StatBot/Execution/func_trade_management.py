from config_execution_api import (
    signal_positive_ticker,
    signal_negative_ticker,
    signal_trigger_thresh,
)
from config_execution_api import (
    tradeable_capital_usdt,
    limit_order_basis,
    session_private,
)
from func_execution_calls import initialize_order_execution
from func_get_zscore import get_latest_zscore
from func_order_review import check_order
from func_price_calls import get_ticker_trade_liquidity
import time


# Manage new trade assessment and order placing
def manage_new_order(kill_switch):
    # Set output variables
    order_long_id = ""
    order_short_id = ""
    signal_side = ""
    hot = False

    # Get and save latest z-score
    zscore, signal_sign_positive = get_latest_zscore()

    # Switch to hot if meets signal threshold
    # Note: You can add in coint-flag check too if you wnat extra vigilence
    if abs(zscore) > signal_trigger_thresh:
        # Active hot trigger
        hot = True
        print("-- Trade Status HOT --")
        print("-- Placing and Monitoring Existing Trades --")

    # Place and manage trades
    if hot and kill_switch == 0:
        # Get trades history for liquidity
        avg_liquidity_ticker_p, last_price_p = get_ticker_trade_liquidity(
            signal_positive_ticker
        )
        avg_liquidity_ticker_n, last_price_n = get_ticker_trade_liquidity(
            signal_negative_ticker
        )

        # Determine long ticker vs short ticker
        if signal_sign_positive:
            long_ticker = signal_positive_ticker
            short_ticker = signal_negative_ticker
            avg_liquidity_long = avg_liquidity_ticker_p
            avg_liquidity_short = avg_liquidity_ticker_n
            last_price_long = last_price_p
            last_price_short = last_price_n
        else:
            long_ticker = signal_negative_ticker
            short_ticker = signal_positive_ticker
            avg_liquidity_long = avg_liquidity_ticker_n
            avg_liquidity_short = avg_liquidity_ticker_p
            last_price_long = last_price_n
            last_price_short = last_price_p

        # Fill Target
        capital_long = tradeable_capital_usdt * 0.5
        capital_short = tradeable_capital_usdt * 0.5
        initial_fill_target_long_usdt = avg_liquidity_long * last_price_long
        initial_fill_target_short_usdt = avg_liquidity_short * last_price_short
        # Get the minimum amount of liquidity as the standard of capital we inject
        initial_capital_injection_usdt = min(
            initial_fill_target_long_usdt, initial_fill_target_short_usdt
        )

        # Ensure initial capital doesn not exceed limits set in configuration
        if limit_order_basis:
            if initial_capital_injection_usdt > capital_long:
                initial_capital_usdt = capital_long
            else:
                # If put market order, it migth eat up the order book if initial_capital_usdt is much smaller than capital_long

                initial_capital_usdt = initial_capital_injection_usdt
        else:
            initial_capital_usdt = capital_long

        # Set remaining capital
        remaining_capital_long = capital_long
        remaining_capital_short = capital_short

        # Trade unitl filled or signal is false
        order_status_long = ""
        order_status_short = ""
        counts_long = 0
        counts_short = 0
        while kill_switch == 0:
            # Place order - long
            if counts_long == 0:
                order_long_id = initialize_order_execution(
                    long_ticker, "Long", initial_capital_usdt
                )
                counts_long = 1 if order_long_id else 0
                remaining_capital_long = remaining_capital_long - initial_capital_usdt

            # Place order - short
            if counts_short == 0:
                order_short_id = initialize_order_execution(
                    short_ticker, "Short", initial_capital_usdt
                )
                counts_short = 1 if order_short_id else 0
                remaining_capital_short = remaining_capital_short - initial_capital_usdt

            # Update signal side
            if zscore > 0:
                signal_side = "positive"
            else:
                signal_side = "negative"

            # Handle kill siwtch for market orders
            if not limit_order_basis and counts_long and counts_short:
                kill_switch = 1

            # Allow for time to register the limit orders
            time.sleep(3)

            # Check limit orders and ensure z_score is still within range
            zscore_new, signal_sign_p_new = get_latest_zscore()

            if kill_switch == 0:
                if (
                    abs(zscore_new) > signal_trigger_thresh * 0.9
                    and signal_sign_p_new == signal_sign_positive
                ):
                    # Check long order status
                    if counts_long == 1:
                        order_status_long = check_order(
                            long_ticker, order_long_id, remaining_capital_long, "Long"
                        )
                    # Chedc short order status

                    if counts_short == 1:
                        order_status_short = check_order(
                            short_ticker,
                            order_short_id,
                            remaining_capital_short,
                            "Short",
                        )

                    # If orders still active, do nothing

                    if (
                        order_status_long == "Order Active"
                        or order_status_short == "Order Active"
                    ):
                        continue

                    # If orders still partial fill, do nothing

                    if (
                        order_status_long == "Partial Fill"
                        or order_status_short == "Partial Fill"
                    ):
                        continue

                    # If orders trade complete, do nohting - stop trading
                    if (
                        order_status_long == "Trade Complete"
                        and order_status_short == "Trade Complete"
                    ):
                        kill_switch = 1
                    # If position filled - place another trade
                    if (
                        order_status_long == "Position Filled"
                        and order_status_short == "Position Filled"
                    ):
                        counts_long = 0
                        counts_short = 0

                    # If order is cancelled for long - try again
                    if order_status_long == "Try Again":
                        counts_long = 0

                    # If order is cancelled for short - try again

                    if order_status_short == "Try Again":
                        counts_short = 0
                else:
                    # Signal no longer in our favor, so stop trading
                    # Cancel all active orders
                    session_private.cancel_all_active_orders(
                        symbol=signal_positive_ticker
                    )
                    session_private.cancel_all_active_orders(
                        symbol=signal_negative_ticker
                    )
                    kill_switch = 1

    if kill_switch == 1:
        # Mean reversion is happened
        if signal_side == "positive" and zscore < 0:
            kill_switch = 2

        if signal_side == "negative" and zscore > 0:
            kill_switch = 2

    # Output status

    return kill_switch
