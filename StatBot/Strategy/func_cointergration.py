import math

from statsmodels.tsa.stattools import coint
from config_strategy_api import z_score_window
import statsmodels.api as sm
import numpy as np
import pandas as pd


# Zero Crossing
def calc_zero_cross(spread):
    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
    return zero_crossings


# Calculate Z-Score:
def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center=False, window=1).mean()
    df["ZSCORE"] = (x - mean) / std

    return df["ZSCORE"].astype(float)


# Calculate Spread
def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - pd.Series(series_2) * hedge_ratio
    return spread


# Calculate cointegrated pairs
def calculate_cointegration(series_1, series_2):
    coint_flag = False

    coint_res = coint(series_1, series_2)

    coint_t, p_value, critical_value = coint_res[0], coint_res[1], coint_res[2][1]

    # Hedge Ratio
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)

    zero_crossings = calc_zero_cross(spread)

    # Cointegration check
    if p_value < 0.5 and coint_t < critical_value:
        coint_flag = True

    return (
        coint_flag,
        round(p_value, 2),
        round(coint_t, 2),
        round(critical_value, 2),
        round(hedge_ratio, 2),
        zero_crossings,
    )


# Put Close prices into a list
def extract_close_prices(prices):
    close_prices = []

    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])

    return close_prices


def get_cointegrated_pairs(prices):
    coint_pair_list = []
    included_list = []

    for sym_1 in prices.keys():
        # Check each coin against the first(sym_1)

        for sym_2 in prices.keys():
            if sym_2 != sym_1:
                # Get Unique Comnination id and ensure one off check

                pair1, pair2 = "".join([sym_1, sym_2]), "".join([sym_2, sym_1])

                if pair1 in included_list or pair2 in included_list:
                    break  # continue

                included_list.append(pair1)
                included_list.append(pair2)

                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])

                # Check for cointegration and add cointegrated pair
                (
                    coint_flag,
                    p_value,
                    t_value,
                    c_value,
                    hedge_ratio,
                    zero_crossings,
                ) = calculate_cointegration(series_1, series_2)

                # print(coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossings)

                if coint_flag:
                    coint_pair_list.append(
                        {
                            "sym1": sym_1,
                            "sym2": sym_2,
                            "p_value": p_value,
                            "t_value": t_value,
                            "c_value": c_value,
                            "hedge_ratio": hedge_ratio,
                            "zero_crossings": zero_crossings,
                        }
                    )

    df_coint = pd.DataFrame(coint_pair_list)

    df_coint = df_coint.sort_values("zero_crossings", ascending=False)

    df_coint.to_csv("F:\Learn\quant\data\\2_cointergrated_pairs.csv")
    return df_coint
