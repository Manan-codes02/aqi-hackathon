import pandas as pd

delhi = pd.read_csv('delhi_clean.csv')
print("Minimum AQI in 5 years of real data:", delhi['AQI'].min())
print("Maximum AQI in 5 years of real data:", delhi['AQI'].max())

# Check specifically what AQI looked like in past monsoon seasons (June-Sept)
delhi['Date'] = pd.to_datetime(delhi['Date'])
delhi['Month'] = delhi['Date'].dt.month
monsoon = delhi[delhi['Month'].isin([6,7,8,9])]
print("\nMonsoon season (Jun-Sep) AQI stats across all 5 years:")
print(monsoon['AQI'].describe())