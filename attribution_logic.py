import pandas as pd

STATION_NAMES = {
    # Delhi - all 36 stations
    'DL001':'Alipur','DL002':'Anand Vihar','DL004':'Aya Nagar',
    'DL005':'Bawana','DL006':'Burari Crossing','DL007':'CRRI Mathura Road',
    'DL008':'DTU','DL009':'Dr. Karni Singh Range','DL010':'Dwarka Sector 8',
    'DL011':'East Arjun Nagar','DL012':'IGI Airport T3','DL013':'IHBAS Dilshad Garden',
    'DL014':'ITO','DL015':'Jahangirpuri','DL016':'JLN Stadium',
    'DL017':'Lodhi Road','DL018':'Major Dhyan Chand Stadium','DL019':'Mandir Marg',
    'DL020':'Mundka','DL021':'NSIT Dwarka','DL022':'Najafgarh',
    'DL023':'Narela','DL024':'Nehru Nagar','DL025':'North Campus DU',
    'DL026':'Okhla Phase-2','DL027':'Patparganj','DL028':'Punjabi Bagh',
    'DL029':'Pusa DPCC','DL030':'Pusa IMD','DL031':'R K Puram',
    'DL032':'Rohini','DL033':'Shadipur','DL034':'Sirifort',
    'DL035':'Sonia Vihar','DL036':'Sri Aurobindo Marg','DL037':'Vivek Vihar',
    'DL038':'Wazirpur',
    # Bengaluru - 10 stations
    'KA002':'BTM Layout','KA003':'BWSSB Kadabesanahalli','KA004':'Bapuji Nagar',
    'KA005':'City Railway Station','KA006':'Hebbal','KA007':'Hombegowda Nagar',
    'KA008':'Jayanagar 5th Block','KA009':'Peenya','KA010':'Sanegurava Halli',
    'KA011':'Silk Board',
}

def load_zone_data(city='Delhi'):
    if city == 'Delhi':
        return pd.read_csv('delhi_station_zones.csv')
    elif city == 'Bengaluru':
        return pd.read_csv('bengaluru_station_zones.csv')
    else:
        raise ValueError(f"Unknown city: {city}")

def get_zone_insight(station_id, city='Delhi'):
    df = load_zone_data(city)
    station_rows = df[df['StationId'] == station_id]
    if station_rows.empty:
        return {"error": f"Station {station_id} not found"}

    zone = station_rows['Zone'].iloc[0]
    station_avg_aqi = station_rows['AQI'].mean()
    overall_avg = df['AQI'].mean()
    diff_from_overall = station_avg_aqi - overall_avg
    percent_diff = (diff_from_overall / overall_avg) * 100

    if percent_diff > 10:
        insight = f"This area ({zone}) shows AQI {percent_diff:.1f}% HIGHER than average — likely linked to {zone.lower()} activity."
    elif percent_diff < -10:
        insight = f"This area ({zone}) shows AQI {abs(percent_diff):.1f}% LOWER than average — relatively cleaner zone."
    else:
        insight = f"This area ({zone}) shows AQI close to the monitored-zone average."

    return {
        "station_id": station_id,
        "zone_type": zone,
        "average_aqi": round(station_avg_aqi, 1),
        "city_average_aqi": round(overall_avg, 1),
        "insight": insight
    }

if __name__ == "__main__":
    print("=== Delhi test ===")
    for sid in ['DL002', 'DL030']:
        print(get_zone_insight(sid, city='Delhi'))

    print("\n=== Bengaluru test ===")
    for sid in ['KA005', 'KA008']:
        print(get_zone_insight(sid, city='Bengaluru'))