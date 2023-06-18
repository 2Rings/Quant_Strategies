
from config_execution_api import signal_positive_ticker, signal_negative_ticker, signal_trigger_thresh
from config_execution_api import tradeable_capital_usdt, limit_order_basis, session_private
from func_execution_calls import initialize_order_execution
from func_get_zscore import get_latest_zscore
from func_order_review import check_order
from func_price_calls import get_ticker_trade_liquidity
import time

# Manage new trade assessment and order placing
def manage_new_order(kill_switch):
    return 0