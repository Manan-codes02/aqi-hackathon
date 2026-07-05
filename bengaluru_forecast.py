import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

bengaluru = pd.read_csv('bengaluru_clean.csv')
data = bengaluru[['Date', 'AQI']].rename(columns={'Date': 'ds', 'AQI': 'y'})
data['ds'] = pd.to_datetime(data['ds'])

model = Prophet()
model.fit(data)

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
forecast['yhat'] = forecast['yhat'].clip(lower=20)
forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=20)
forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=20)

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))

fig = model.plot(forecast)
plt.title("Bengaluru AQI Forecast")
plt.savefig('bengaluru_forecast_plot.png')
plt.show()
print("Done")