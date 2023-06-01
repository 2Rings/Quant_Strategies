
#Calculate cointegrated pairs

def get_cointegrated_pairs(prices):
    coint_pair_lsit = []
    included_lsit = []

    for sym_1 in prices.keys():
        print(sym_1)