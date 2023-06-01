import math

from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
#Calculate Spread
def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.DataFrame(series_1) - pd.DataFrame(series_2) * hedge_ratio
    return spread

#Calculate cointegrated pairs
def calculate_cointegration(series_1, series_2):
    coint_flag = 0

    coint_res = coint(series_1, series_2)

    coint_t, p_value, critical_value = coint_res[0], coint_res[1], coint_res[2][1]

    # Hedge Ratio
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)  

    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
    
    #Cointegration check
    if p_value < 0.5 and coint_t < critical_value:
        coint_flag = 1

    return (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2), zero_crossings)






# Put Close prices into a list
def extract_close_prices(prices):
    close_prices = []

    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])

    return close_prices


def get_cointegrated_pairs(prices):
    coint_pair_lsit = []
    included_list = []

    for sym_1 in prices.keys():
        # Check each coin against the first(sym_1)
        
        for sym_2 in prices.keys():
            if sym_2 != sym_1:
                # Get Unique Comnination id and ensure one off check
                
                pair1, pair2 = "".join([sym_1, sym_2]), "".join([sym_2, sym_1])

                if pair1 in included_list or pai2 in included_list:
                    continue

                included_list.append(pair1)
                included_list.append(pair2)

                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])

