import pandas as pd

station_day = pd.read_csv('station_day.csv')
stations = pd.read_csv('stations.csv')

zone_map = {
    'KA002': 'Residential',   # BTM Layout
    'KA003': 'Industrial',    # BWSSB Kadabesanahalli
    'KA004': 'Residential',   # Bapuji Nagar
    'KA005': 'Traffic',       # City Railway Station
    'KA006': 'Traffic',       # Hebbal
    'KA007': 'Residential',   # Hombegowda Nagar
    'KA008': 'Residential',   # Jayanagar 5th Block
    'KA009': 'Industrial',    # Peenya
    'KA010': 'Industrial',    # Sanegurava Halli
    'KA011': 'Traffic',       # Silk Board
}

station_names = {
    'KA002': 'BTM Layout',
    'KA003': 'BWSSB Kadabesanahalli',
    'KA004': 'Bapuji Nagar',
    'KA005': 'City Railway Station',
    'KA006': 'Hebbal',
    'KA007': 'Hombegowda Nagar',
    'KA008': 'Jayanagar 5th Block',
    'KA009': 'Peenya',
    'KA010': 'Sanegurava Halli',
    'KA011': 'Silk Board',
}

filtered = station_day[station_day['StationId'].isin(zone_map.keys())].copy()
filtered['Zone'] = filtered['StationId'].map(zone_map)
filtered['StationName'] = filtered['StationId'].map(station_names)
filtered = filtered.dropna(subset=['AQI'])

zone_avg = filtered.groupby('Zone')['AQI'].mean().sort_values(ascending=False)
print("=== Average AQI by Zone Type (Bengaluru) ===")
print(zone_avg.round(1))

print("\n=== Number of readings per zone ===")
print(filtered.groupby('Zone')['AQI'].count())

station_avg = filtered.groupby(['StationId', 'StationName', 'Zone'])['AQI'].mean()
station_avg = station_avg.reset_index().sort_values('AQI', ascending=False)
station_avg['AQI'] = station_avg['AQI'].round(1)
print("\n=== All 10 stations ranked by average AQI ===")
print(station_avg[['StationName', 'Zone', 'AQI']].to_string(index=False))

filtered.to_csv('bengaluru_station_zones.csv', index=False)
station_avg.to_csv('bengaluru_station_summary.csv', index=False)
print("\nSaved bengaluru_station_zones.csv and bengaluru_station_summary.csv")