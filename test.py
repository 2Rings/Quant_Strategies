# test
from scipy import stats

def analyze_alpha(expected_returns):
    t_val, p_val = stats.ttest_1samp(expected_returns, popmean=0)
    return t_val, p_val/2.0