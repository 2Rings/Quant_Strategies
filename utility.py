import pandas as pd
import numpy as np
def resample_prices(prices: pd.DataFrame, freq = 'M', type = 'last') -> pd.DataFrame:
    if type == 'last':
        prices_resampled = prices.resample(rule=freq).last()

    return prices_resampled

def compute_log_return(prices: pd.DataFrame )->pd.DataFrame:
    shift_prices = prices.shift(1)
    log_returns  = np.log(prices) - np.log(shift_prices)
    return log_returns

def shift_returns(returns: pd.DataFrame, shift_n: int) -> pd.DataFrame:
    shifted_returns = returns.shift(shift_n)
    return shift_returns

def get_top_n(df_prices, top_n):
    tmp = df_prices
    top_prices[:] = 0

    for date, prices in df_prices.iterrows():
        top_prices.loc[date, prices.dropna().nlargest(top_n).index] = 1

    return top_prices.astype('int64')

def long_short_returns(long_pos, short_pos, returns, pos_count):
    long_returns = returns.mask(~long_pos.astype(bool)).fillna(0)
    short_returns = returns.mask(~short_pos.astype(bool)).fillna(0)

    portfolio_returns = (long_returns - short_returns)/pos_count
    return portfolio_returns

def portfolio_stats(portfolio_returns: pd.DataFrame, freq = 12):
    expected_returns = portfolio_returns.T.sum().dropna()
    port_mean = expected_returns.mean()

    #unbiased standard error
    port_ste  = expected_returns.sem()

    annual_rate = (np.exp(portfolio_returns*freq) - 1) *100

    print("""
            Mean:                       {:.6f}
            Standard Error:             {:.6f}
            Annualized Rate of Return:  {:.2f}%
            """.format(port_mean, port_ste, annual_rate))