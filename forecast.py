import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load cleaned data
delhi = pd.read_csv('delhi_clean.csv')

# Prophet requires specific column names: 'ds' for date, 'y' for the value to predict
data = delhi[['Date', 'AQI']].rename(columns={'Date': 'ds', 'AQI': 'y'})
data['ds'] = pd.to_datetime(data['ds'])

# Create and train the model
model = Prophet()
model.fit(data)

# Create future dates to predict (next 30 days beyond your data)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

#This forces any -ve prediction to become 0 (as negative AQI is meaningless)
forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
forecast['yhat'] = forecast['yhat'].clip(lower=0)

# Show the last 10 predicted rows (the actual future predictions)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))

# Plot the forecast
fig = model.plot(forecast)
plt.title("Delhi AQI Forecast")
plt.xlabel("Date")
plt.ylabel("AQI")
plt.savefig('forecast_plot.png')
plt.show()