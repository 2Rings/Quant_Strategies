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

        print(avg_liquidity_ticker_p, avg_liquidity_ticker_n)

    print(zscore, signal_sign_positive)
