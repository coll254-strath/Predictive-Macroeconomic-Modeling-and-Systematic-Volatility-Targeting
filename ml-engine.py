
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from project_sentinel.config import CONFIG

def build_ml_features(df_stationary):
    # Creates lagged features to eliminate lookahead bias.
    df_ml = df_stationary.copy()
    df_ml['Lagged_GDP'] = df_ml['GDP_Growth'].shift(1)
    df_ml['Lagged_Returns'] = df_ml['SP500_Returns'].shift(1)
    df_ml['Lagged_dInflation'] = df_ml['d_Inflation'].shift(1)
    df_ml['Lagged_dFed'] = df_ml['d_Fed_Funds'].shift(1)
    df_ml['Lagged_Vol'] = df_ml['Conditional_Vol_GARCH'].shift(1)
    return df_ml.dropna()

def train_predict_rf(df_ml):
    # Splits sequentially, trains Random Forest model, and predicts out-of-sample returns.
    features = ['Lagged_GDP', 'Lagged_Returns', 'Lagged_dInflation', 'Lagged_dFed', 'Lagged_Vol']
    X = df_ml[features]
    y = df_ml['SP500_Returns']

    split_idx = int(len(X) * CONFIG['TRAIN_SPLIT_RATIO'])

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    model = RandomForestRegressor(
        n_estimators=CONFIG['RF_ESTIMATORS'],
        max_depth=CONFIG['RF_MAX_DEPTH'],
        random_state=CONFIG['SEED']
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    # Package results
    results_df = pd.DataFrame({
        'Actual_Return': y_test,
        'Predicted_Return': predictions
    }, index=y_test.index)

    return results_df, model.feature_importances_, features
