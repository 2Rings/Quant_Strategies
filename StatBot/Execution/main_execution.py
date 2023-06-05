# Remove panda Future warnings
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# General imports
from config_execution_api import signal_positive_ticker, signal_negative_ticker
from func_position_calls import open_position_confirmation, active_position_confirmation
from func_trade_management import manage_new_trades
from func_execution_calls import set_leverage
from func_close_positions import close_all_positions
from func_save_status import save_status
import time

"""
    RUN STATBOT
"""

if __name__ == "__main__":
    pass