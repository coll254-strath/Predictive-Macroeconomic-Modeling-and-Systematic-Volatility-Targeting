
import numpy as np
import pandas as pd

def simulate_tactical_strategy(results_df):
    # Applies the trading logic:
    # If next period forecasted return is positive, hold stock.
    # Else, shift 100% to risk-free cash (0% return).
    results_df['Strategy_Return'] = np.where(
        results_df['Predicted_Return'] > 0,
        results_df['Actual_Return'],
        0.0
    )

    # Calculate cumulative returns
    results_df['Cum_Market'] = (1 + results_df['Actual_Return']).cumprod() - 1
    results_df['Cum_Strategy'] = (1 + results_df['Strategy_Return']).cumprod() - 1
    return results_df
