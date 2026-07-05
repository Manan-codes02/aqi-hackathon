import pandas as pd

stations = pd.read_csv('stations_2024.csv')  # rename the new stations.csv first
print(stations['City'].value_counts().sort_values(ascending=False))
print("\nTotal stations:", len(stations))

# # Load the new dataset - update filename to whatever it downloaded as
# df = pd.read_csv('city_day_2024.csv')  # rename to this after downloading

# print("Columns:", df.columns.tolist())
# date_col = 'Datetime' if 'Datetime' in df.columns else 'Date'
# print("Date range:", df[date_col].min(), "to", df[date_col].max())
# print("\nCities available:")
# print(sorted(df['City'].unique()))
# print("\nShape:", df.shape)

# for city in ['Delhi', 'Bengaluru', 'Bangalore']:
#     city_data = df[df['City'] == city]
#     if len(city_data) > 0:
#         print(f"\n{city}: {len(city_data)} rows, AQI missing: {city_data['AQI'].isna().sum()}")


# stations = pd.read_csv('stations.csv')
# delhi_stations = stations[stations['City'] == 'Delhi']
# print(delhi_stations[['StationId', 'StationName']])

# # Now check station-level AQI data
# station_day = pd.read_csv('station_day.csv')
# print(station_day.head())
# print(station_day['StationId'].nunique())


# stations = pd.read_csv('stations.csv')
# print(stations.head(20))
# print(stations.shape)
# print(stations['City'].unique() if 'City' in stations.columns else stations.columns)


# delhi = pd.read_csv('delhi_clean.csv')
# delhi['Date'] = pd.to_datetime(delhi['Date'])

# # Fill missing AQI values using interpolation (estimate based on nearby days)
# delhi['AQI'] = delhi['AQI'].interpolate(method='linear')

# # Double check no missing values remain
# print("Missing AQI values after fixing:", delhi['AQI'].isna().sum())

# # Save the final cleaned version
# delhi.to_csv('delhi_clean.csv', index=False)
# print("Updated delhi_clean.csv saved")


# # Filter only Delhi rows
# delhi = df[df['City'] == 'Delhi'].copy()

# # Convert Date column to actual datetime format
# delhi['Date'] = pd.to_datetime(delhi['Date'])

# # Sort by date (just to be safe)
# delhi = delhi.sort_values('Date')

# # Check how many missing values remain in AQI after filtering
# print(delhi[['Date', 'AQI']].isna().sum())

# # Check the date range available
# print(delhi['Date'].min(), "to", delhi['Date'].max())

# # Save this cleaned Delhi-only file for next steps
# delhi.to_csv('delhi_clean.csv', index=False)


# # Check how much AQI data is missing per city
# missing_summary = df.groupby('City')['AQI'].apply(lambda x: x.notna().sum())
# print(missing_summary.sort_values(ascending=False))

# print(df.head())
# print(df['City'].unique())
# print(df.shape)