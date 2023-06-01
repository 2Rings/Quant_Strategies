"""
    Strategy Code
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
import pandas as pd




if __name__ == "__main__":
    # STEP 1 - Get list of symbol
    print("Getting symbols...")
    sym_response = get_tradeable_symbols()

    # STEP 2 - Construct and save price history
    print("Constructing and saving prices data to JSON...")

    if len(sym_response) > 0:
        store_price_history(sym_response)

