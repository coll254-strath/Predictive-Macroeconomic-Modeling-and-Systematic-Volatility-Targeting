
from project_sentinel.config import CONFIG
from project_sentinel.data_engine import fetch_or_simulate_data
from project_sentinel.econometrics import (
    run_stationarity_tests,
    create_stationary_dataframe,
    fit_var_model,
    extract_garch_volatility
)
from project_sentinel.ml_engine import build_ml_features, train_predict_rf
from project_sentinel.portfolio import simulate_tactical_strategy

def main():
    print("Initializing Project Sentinel Pipeline...")

    # 1. Ingest Data
    df = fetch_or_simulate_data(api_key=CONFIG['FRED_API_KEY'])

    # 2. Stationarity Tests & Differencing
    print("\n--- 1. Diagnostic Checks ---")
    adf_results = run_stationarity_tests(df)
    for var, res in adf_results.items():
        status = "Stationary" if res['stationary'] else "Non-Stationary"
        print(f"Variable: {var:<18} | ADF Stat: {res['adf_stat']:>8.4f} | P-Value: {res['p_value']:>6.4f} | Status: {status}")

    df_stationary = create_stationary_dataframe(df)

    # 3. Fit Econometric VAR Model
    print("\n--- 2. Fitting Joint VAR Model ---")
    var_res = fit_var_model(df_stationary, lags=1)
    print("VAR parameters successfully estimated.")

    # 4. Extract GARCH Volatility
    print("\n--- 3. Estimating Market Volatility (GARCH) ---")
    df_stationary['Conditional_Vol_GARCH'] = extract_garch_volatility(df_stationary['SP500_Returns'])
    print("GARCH(1,1) conditional volatility successfully calculated.")

    # 5. Feature Engineering & ML Predictions
    print("\n--- 4. ML Engine Modeling & Prediction ---")
    df_ml = build_ml_features(df_stationary)
    results_df, importances, features = train_predict_rf(df_ml)

    # Print feature importance
    for feat, imp in zip(features, importances):
        print(f"Predictor: {feat:<18} | Model Importance: {imp:.4f}")

    # 6. Portfolio Simulator
    print("\n--- 5. Simulating Systematic Tactical Allocation Strategy ---")
    perf_df = simulate_tactical_strategy(results_df)

    final_market_ret = perf_df['Cum_Market'].iloc[-1] * 100
    final_strat_ret = perf_df['Cum_Strategy'].iloc[-1] * 100

    print(f"\n--- [RESULT SUMMARY] ---")
    print(f"Out-of-Sample Buy & Hold Return:      {final_market_ret:.2f}%")
    print(f"Out-of-Sample Sentinel Strategy Return: {final_strat_ret:.2f}%")
    print("=========================================================")

if __name__ == '__main__':
    main()
