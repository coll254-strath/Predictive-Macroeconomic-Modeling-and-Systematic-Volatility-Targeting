Project Overview
Standard "Buy & Hold" strategies expose investor capital to 100% of market drawdowns, leaving portfolios highly vulnerable during macroeconomic crises.

Project Sentinel solves this problem by establishing a systematic bridge between macroeconomic indicators (GDP, Inflation, Interest Rates) and financial market volatility. By modeling these dynamic interactions, our system identifies high-risk economic regimes and dynamically shifts assets into defensive cash positions—safeguarding capital without sacrificing long-term equity growth.

🎯 Key Objectives
Dynamic Regime Identification: Quantify and track the transmission of macroeconomic shocks into equity market returns.
Volatility Clustering Capture: Model persistent financial market fear using asymmetric volatility frameworks.
Systematic Portfolio Shielding: Build and backtest a machine-learning-driven tactical asset allocation strategy that switches to cash during high-risk regimes.
🛠 System Architecture
The pipeline is structured into four core stages:

  [Data Ingestion]     ->      [Econometric Modeling]      ->       [Regime Forecasting]       ->    [Tactical Execution]
(FRED API / Synthetic)       (Stationarity, VAR, GARCH)           (Random Forest Regressor)         (Asset Allocation Engine)
Ingestion & Synthesis: Pulls live macro-financial data from the Federal Reserve Economic Data (FRED) API or simulates a statistically rigorous synthetic environment with built-in macro-economic correlations.
Econometric Engine: Tests time-series stationarity (ADF Test), models joint dynamics via Vector Autoregression (VAR), and extracts the underlying "fear index" via a GARCH(1,1) model.
Machine Learning Layer: Uses lagged macroeconomic indicators and GARCH conditional volatility to train a predictive Random Forest Regressor.
Portfolio Simulator: Translates predictions into a binary systematic trading strategy (Long S&P 500 vs. Cash) and evaluates out-of-sample performance.
🔬 Core Methodologies
1. Vector Autoregression (VAR)
To capture the joint dynamic paths of macroeconomic variables without imposing strict structural assumptions, we model the system as:
Yt=c+A1Yt−1+⋯+ApYt−p+εt 
This allows us to construct Impulse Response Functions (IRFs) to simulate macroeconomic "stress tests" (e.g., how an inflation shock impacts stock returns over subsequent quarters).

2. GARCH Volatility Modeling
To model "volatility clustering" (the tendency of extreme market moves to be followed by more extreme moves), we implement a GARCH(1,1) model on stock returns:
\sigma^t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2 
This extracts the conditional volatility used as a key risk parameter in our predictive model.

3. Machine Learning Tactical Strategy
Predictors: Lagged GDP Growth, Lagged Returns, Lagged Changes in Inflation ( d\_Inflation ), Lagged Changes in Federal Funds ( d\_Fed\_Funds ), and Lagged GARCH Volatility.
Decision Rule: $$\text{Position}_{t+1} =
{1.0 (100% Long S&P 500)0.0 (100% Cash)if R^t+1>0if R^t+1≤0 
$$
📊 Performance & Investment Insights
During out-of-sample testing, the Project Sentinel Macro-Driven GARCH Strategy demonstrated significant structural advantages over the benchmark Index:

Downside Capital Protection: During major macroeconomic downturns, the model successfully pivoted to cash (represented by flat horizontal lines on the performance chart), bypassing steep drawdowns.
Wealth Preservation: Avoiding compounding losses allowed the strategy to significantly outperform the simple "Buy & Hold" benchmark on a risk-adjusted basis.
