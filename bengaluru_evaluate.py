import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error
import numpy as np

bengaluru = pd.read_csv('bengaluru_clean.csv')
data = bengaluru[['Date', 'AQI']].rename(columns={'Date': 'ds', 'AQI': 'y'})
data['ds'] = pd.to_datetime(data['ds'])

# Test on winter period (same approach as Delhi)
test = data[(data['ds'] >= '2016-12-01') & (data['ds'] <= '2016-12-30')].reset_index(drop=True)
train = data[data['ds'] < '2016-12-01'].reset_index(drop=True)

model = Prophet()
model.fit(train)

future = model.make_future_dataframe(periods=len(test))
forecast = model.predict(future)
predicted = forecast[['ds', 'yhat']].tail(len(test)).reset_index(drop=True)
predicted['yhat'] = predicted['yhat'].clip(lower=20)

actual = test['y'].reset_index(drop=True)

prophet_rmse = np.sqrt(mean_squared_error(actual, predicted['yhat']))
last_known = train['y'].iloc[-1]
baseline_rmse = np.sqrt(mean_squared_error(actual, [last_known]*len(test)))

print(f"Bengaluru Prophet RMSE: {prophet_rmse:.2f}")
print(f"Bengaluru Baseline RMSE: {baseline_rmse:.2f}")

if prophet_rmse < baseline_rmse:
    improvement = ((baseline_rmse - prophet_rmse) / baseline_rmse) * 100
    print(f"Model is {improvement:.1f}% better than naive baseline")
else:
    print("Model not beating baseline on this test period")

# import pandas as pd
# import numpy as np

# bengaluru = pd.read_csv('bengaluru_clean.csv')
# bengaluru['Date'] = pd.to_datetime(bengaluru['Date'])
# bengaluru = bengaluru.sort_values('Date')
# bengaluru['daily_change'] = bengaluru['AQI'].diff().abs()
# bengaluru['Month'] = bengaluru['Date'].dt.month
# bengaluru['Year'] = bengaluru['Date'].dt.year

# monthly_volatility = bengaluru.groupby(['Year','Month'])['daily_change'].mean()
# print("Most volatile months (highest day-to-day AQI change):")
# print(monthly_volatility.sort_values(ascending=False).head(10))