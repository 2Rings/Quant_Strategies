"""
    Strategy Code
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointergration import get_cointegrated_pairs
import pandas as pd
import json



if __name__ == "__main__":

    
    # # STEP 1 - Get list of symbol
    # print("Getting symbols...")
    # sym_response = get_tradeable_symbols()

    # # STEP 2 - Construct and save price history
    # print("Constructing and saving prices data to JSON...")

    # if len(sym_response) > 0:
    #     store_price_history(sym_response)

    # STEP 3 - Find Cointegrated pairs
    print("Calculating co-intergration...")

    with open("F:\Learn\quant\data\\1_price_list.json", "r") as json_file:
        price_data = json.load(json_file)

        if len(price_data) > 0:
            coint_pairs = get_cointegrated_pairs(price_data)
