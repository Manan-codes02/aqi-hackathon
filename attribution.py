import pandas as pd

# Load station data - note: station_day.csv needs to be in folder temporarily to run this
# After running, move station_day.csv back out of the folder
station_day = pd.read_csv('station_day.csv')
stations = pd.read_csv('stations.csv')

# All 36 Delhi stations tagged with zone types
zone_map = {
    # Already done (original 10)
    'DL002': 'Traffic',        # Anand Vihar
    'DL014': 'Traffic',        # ITO
    'DL028': 'Traffic',        # Punjabi Bagh
    'DL025': 'Institutional',  # North Campus, DU
    'DL012': 'Traffic',        # IGI Airport T3
    'DL022': 'Industrial',     # Najafgarh
    'DL026': 'Industrial',     # Okhla Phase-2
    'DL038': 'Industrial',     # Wazirpur
    'DL019': 'Residential',    # Mandir Marg
    'DL017': 'Residential',    # Lodhi Road

    # New 26 stations
    'DL001': 'Residential',    # Alipur
    'DL004': 'Residential',    # Aya Nagar
    'DL005': 'Industrial',     # Bawana
    'DL006': 'Residential',    # Burari Crossing
    'DL007': 'Institutional',  # CRRI Mathura Road
    'DL008': 'Institutional',  # DTU
    'DL009': 'Institutional',  # Dr. Karni Singh Shooting Range
    'DL010': 'Residential',    # Dwarka Sector 8
    'DL011': 'Residential',    # East Arjun Nagar
    'DL013': 'Institutional',  # IHBAS Dilshad Garden
    'DL015': 'Industrial',     # Jahangirpuri
    'DL016': 'Institutional',  # JLN Stadium
    'DL018': 'Institutional',  # Major Dhyan Chand Stadium
    'DL020': 'Industrial',     # Mundka
    'DL021': 'Institutional',  # NSIT Dwarka
    'DL023': 'Industrial',     # Narela
    'DL024': 'Residential',    # Nehru Nagar
    'DL027': 'Industrial',     # Patparganj
    'DL029': 'Institutional',  # Pusa DPCC
    'DL030': 'Institutional',  # Pusa IMD
    'DL031': 'Residential',    # R K Puram
    'DL032': 'Residential',    # Rohini
    'DL033': 'Traffic',        # Shadipur
    'DL034': 'Institutional',  # Sirifort
    'DL035': 'Residential',    # Sonia Vihar
    'DL036': 'Residential',    # Sri Aurobindo Marg
    'DL037': 'Residential',    # Vivek Vihar
}

# Station display names
station_names = {
    'DL001': 'Alipur', 'DL002': 'Anand Vihar', 'DL004': 'Aya Nagar',
    'DL005': 'Bawana', 'DL006': 'Burari Crossing', 'DL007': 'CRRI Mathura Road',
    'DL008': 'DTU', 'DL009': 'Dr. Karni Singh Range', 'DL010': 'Dwarka Sector 8',
    'DL011': 'East Arjun Nagar', 'DL012': 'IGI Airport T3', 'DL013': 'IHBAS Dilshad Garden',
    'DL014': 'ITO', 'DL015': 'Jahangirpuri', 'DL016': 'JLN Stadium',
    'DL017': 'Lodhi Road', 'DL018': 'Major Dhyan Chand Stadium', 'DL019': 'Mandir Marg',
    'DL020': 'Mundka', 'DL021': 'NSIT Dwarka', 'DL022': 'Najafgarh',
    'DL023': 'Narela', 'DL024': 'Nehru Nagar', 'DL025': 'North Campus DU',
    'DL026': 'Okhla Phase-2', 'DL027': 'Patparganj', 'DL028': 'Punjabi Bagh',
    'DL029': 'Pusa DPCC', 'DL030': 'Pusa IMD', 'DL031': 'R K Puram',
    'DL032': 'Rohini', 'DL033': 'Shadipur', 'DL034': 'Sirifort',
    'DL035': 'Sonia Vihar', 'DL036': 'Sri Aurobindo Marg', 'DL037': 'Vivek Vihar',
    'DL038': 'Wazirpur',
}

# Filter to our 36 tagged Delhi stations
filtered = station_day[station_day['StationId'].isin(zone_map.keys())].copy()
filtered['Zone'] = filtered['StationId'].map(zone_map)
filtered['StationName'] = filtered['StationId'].map(station_names)
filtered = filtered.dropna(subset=['AQI'])

# Zone-level summary
zone_avg = filtered.groupby('Zone')['AQI'].mean().sort_values(ascending=False)
print("=== Average AQI by Zone Type (all 36 stations) ===")
print(zone_avg.round(1))

print("\n=== Number of readings per zone ===")
print(filtered.groupby('Zone')['AQI'].count())

# Station-level summary (ranked)
station_avg = filtered.groupby(['StationId', 'StationName', 'Zone'])['AQI'].mean()
station_avg = station_avg.reset_index().sort_values('AQI', ascending=False)
station_avg['AQI'] = station_avg['AQI'].round(1)
print("\n=== All 36 stations ranked by average AQI ===")
print(station_avg[['StationName', 'Zone', 'AQI']].to_string(index=False))

# Save for dashboard
filtered.to_csv('delhi_station_zones.csv', index=False)
station_avg.to_csv('delhi_station_summary.csv', index=False)
print("\nSaved delhi_station_zones.csv and delhi_station_summary.csv")