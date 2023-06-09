"""
    Strategy Code
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointergration import get_cointegrated_pairs
from func_plot_trends import plot_trends
import pandas as pd
import json



if __name__ == "__main__":
    data_path = "F:\Learn\quant\data"
    
    # # STEP 1 - Get list of symbol
    # print("Getting symbols...")
    # sym_response = get_tradeable_symbols()

    # # STEP 2 - Construct and save price history
    # print("Constructing and saving prices data to JSON...")

    # if len(sym_response) > 0:
    #     store_price_history(sym_response)

    # STEP 3 - Find Cointegrated pairs

    # print("Calculating co-intergration...")

    # with open("F:\Learn\quant\data\\1_price_list.json", "r") as json_file:
    #     price_data = json.load(json_file)

    #     if len(price_data) > 0:
    #         coint_pairs = get_cointegrated_pairs(price_data)
    
    # print("done.")

    # STEP 4 - Plot trends and save for backtesting
    sym_1 = "MATICUSDT"
    sym_2 = "STXUSDT"
    with open(data_path + "\\1_price_list.json", 'r') as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            plot_trends(sym_1, sym_2, price_data)
