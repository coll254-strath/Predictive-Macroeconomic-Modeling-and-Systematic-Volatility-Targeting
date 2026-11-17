
import numpy as np
import pandas as pd
from fredapi import Fred
from project_sentinel.config import CONFIG

def fetch_or_simulate_data(api_key=None):
    # Tries to pull real economic data from the FRED API.
    # If keys or connection fails, falls back to simulating a realistic macro-financial dataset.
    if api_key:
        try:
            fred = Fred(api_key=api_key)
            df_cpi = fred.get_series('CPIAUCSL', observation_start=CONFIG['START_DATE'])
            df_gdp = fred.get_series('GDPC1', observation_start=CONFIG['START_DATE'])
            df_fed = fred.get_series('FEDFUNDS', observation_start=CONFIG['START_DATE'])
            df_sp = fred.get_series('SP500', observation_start=CONFIG['START_DATE'])

            df = pd.DataFrame({
                'CPI': df_cpi,
                'GDP': df_gdp,
                'FedFunds': df_fed,
                'SP500': df_sp
            })
            df = df.resample('ME').ffill().dropna()
            print("\n[DataEngine] Data successfully ingested from FRED API!")
            # Map to matching column names
            df.columns = ['Inflation_YoY', 'GDP_Growth', 'Fed_Funds_Rate', 'SP500_Returns']
            # Convert prices to returns if necessary
            df['SP500_Returns'] = df['SP500_Returns'].pct_change()
            return df.dropna()
        except Exception as e:
            print(f"\n[DataEngine] FRED API Fetch failed ({e}). Falling back to simulation...")

    # Synthetic fallback simulation
    np.random.seed(CONFIG['SEED'])
    dates = pd.date_range(start=CONFIG['START_DATE'], end=CONFIG['END_DATE'], freq='ME')
    n = len(dates)

    fed_funds = 2.0 + np.cumsum(np.random.normal(0, 0.2, n))
    fed_funds = np.clip(fed_funds, 0.05, 6.0)

    cpi_yoy = 2.0 + 0.3 * fed_funds + np.cumsum(np.random.normal(0, 0.15, n))
    cpi_yoy = np.clip(cpi_yoy, -1.0, 10.0)

    gdp_growth = 2.5 - 0.2 * fed_funds + np.random.normal(0, 0.8, n)

    volatility = np.zeros(n)
    sp_returns = np.zeros(n)
    v_t = 0.02
    for t in range(n):
        v_t = 0.01 + 0.1 * (sp_returns[t-1]**2 if t > 0 else 0) + 0.8 * v_t
        volatility[t] = np.sqrt(v_t)
        mean_return = 0.006 + 0.002 * gdp_growth[t] - 0.001 * cpi_yoy[t]
        sp_returns[t] = mean_return + np.random.normal(0, volatility[t])

    df = pd.DataFrame({
        'GDP_Growth': gdp_growth,
        'Inflation_YoY': cpi_yoy,
        'Fed_Funds_Rate': fed_funds,
        'SP500_Returns': sp_returns
    }, index=dates)
    print("\n[DataEngine] Statistically robust synthetic dataset generated successfully.")
    return df
