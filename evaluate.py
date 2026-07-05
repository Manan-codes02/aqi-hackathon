import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error
import numpy as np

# Load cleaned data
delhi = pd.read_csv('delhi_clean.csv')
data = delhi[['Date', 'AQI']].rename(columns={'Date': 'ds', 'AQI': 'y'})
data['ds'] = pd.to_datetime(data['ds'])

# # Split: use everything except the last 30 days to train, test on last 30 days
# train = data.iloc[:-30]
# test = data.iloc[-30:]

# Test on a winter period instead (more meaningful variation in AQI)
test = data[(data['ds'] >= '2019-12-01') & (data['ds'] <= '2019-12-30')].reset_index(drop=True)
train = data[data['ds'] < '2019-12-01'].reset_index(drop=True)

# Train Prophet on training data only
model = Prophet()
model.fit(train)

# Predict the same 30 days that are in our test set
# future = model.make_future_dataframe(periods=30)
future = model.make_future_dataframe(periods=len(test))
forecast = model.predict(future)
predicted = forecast[['ds', 'yhat']].tail(len(test)).reset_index(drop=True)
predicted['yhat'] = predicted['yhat'].clip(lower=0)

actual = test['y'].reset_index(drop=True)

# Calculate Prophet's error (RMSE)
prophet_rmse = np.sqrt(mean_squared_error(actual, predicted['yhat']))

# Calculate "persistence baseline" - just repeat the last known value
last_known_value = train['y'].iloc[-1]
baseline_predictions = [last_known_value] * 30
baseline_rmse = np.sqrt(mean_squared_error(actual, baseline_predictions))

print(f"Prophet Model RMSE: {prophet_rmse:.2f}")
print(f"Persistence Baseline RMSE: {baseline_rmse:.2f}")

if prophet_rmse < baseline_rmse:
    improvement = ((baseline_rmse - prophet_rmse) / baseline_rmse) * 100
    print(f"✅ Your model is {improvement:.1f}% better than the naive baseline!")
else:
    print("⚠️ Model needs improvement - currently not beating the baseline")