# General imports
from config_execution_api import signal_positive_ticker, signal_negative_ticker
from func_close_positions import close_all_positions
from func_execution_calls import set_leverage
from func_position_calls import open_position_confirmation, active_position_confirmation
from func_save_status import save_status
from func_trade_management import manage_new_trades
import time
# Remove panda Future warnings
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

"""
    RUN STATBOT
"""

if __name__ == "__main__":
    # Initial printout
    print("StatBot initiated...")

    # Initialize Variable
    status_dict = {"message": "Starting..."}
    order_long = {}
    order_short = {}
    signal_sign_positive = False
    kill_swith = 0

    