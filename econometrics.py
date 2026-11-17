
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import VAR
from arch import arch_model

def run_stationarity_tests(df):
    # Performs Augmented Dickey-Fuller (ADF) tests on dataframe columns.
    results = {}
    for col in df.columns:
        res = adfuller(df[col].dropna())
        results[col] = {
            'adf_stat': res[0],
            'p_value': res[1],
            'stationary': res[1] < 0.05
        }
    return results

def create_stationary_dataframe(df):
    # Applies first-differencing to non-stationary variables (CPI/FedFunds).
    df_stat = pd.DataFrame(index=df.index)
    df_stat['GDP_Growth'] = df['GDP_Growth']
    df_stat['SP500_Returns'] = df['SP500_Returns']

    # Compute differences for macro non-stationary metrics
    df_stat['d_Inflation'] = df['Inflation_YoY'].diff()
    df_stat['d_Fed_Funds'] = df['Fed_Funds_Rate'].diff()
    return df_stat.dropna()

def fit_var_model(df_stationary, lags=1):
    # Fits a Vector Autoregression model.
    model = VAR(df_stationary)
    results = model.fit(lags)
    return results

def extract_garch_volatility(returns_series):
    # Fits GARCH(1,1) and extracts conditional volatility scaled appropriately.
    scaled_returns = returns_series * 100
    model = arch_model(scaled_returns, vol='Garch', p=1, q=1, dist='Normal')
    res = model.fit(disp='off')
    # Scale volatility back
    return res.conditional_volatility 
