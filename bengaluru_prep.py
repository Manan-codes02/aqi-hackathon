import pandas as pd

# Load original dataset
df = pd.read_csv('city_day.csv')

# Filter Bengaluru
bengaluru = df[df['City'] == 'Bengaluru'].copy()
bengaluru['Date'] = pd.to_datetime(bengaluru['Date'])
bengaluru = bengaluru.sort_values('Date')

# Check missing values
print(f"Total rows: {len(bengaluru)}")
print(f"Date range: {bengaluru['Date'].min()} to {bengaluru['Date'].max()}")
print(f"Missing AQI: {bengaluru['AQI'].isna().sum()}")

# Fill missing values
bengaluru['AQI'] = bengaluru['AQI'].interpolate(method='linear')
print(f"Missing AQI after fix: {bengaluru['AQI'].isna().sum()}")
print(f"Min AQI: {bengaluru['AQI'].min()}, Max AQI: {bengaluru['AQI'].max()}")

# Handle remaining missing values at edges
bengaluru['AQI'] = bengaluru['AQI'].ffill()
bengaluru['AQI'] = bengaluru['AQI'].bfill()
print(f"Missing AQI after ffill/bfill: {bengaluru['AQI'].isna().sum()}")

# Save
bengaluru.to_csv('bengaluru_clean.csv', index=False)
print("Saved bengaluru_clean.csv")