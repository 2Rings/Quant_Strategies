
from config_execution_api import signal_positive_ticker, signal_negative_ticker, signal_trigger_thresh
from config_execution_api import tradeable_capital_usdt, limit_order_basis, session_private
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
        avg_liquidity_ticker_p, last_price_p = get_ticker_trade_liquidity(signal_positive_ticker)
        avg_liquidity_ticker_n, last_price_n = get_ticker_trade_liquidity(signal_negative_ticker)

        print(avg_liquidity_ticker_p, avg_liquidity_ticker_n)

    print(zscore, signal_sign_positive)