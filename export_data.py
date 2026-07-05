import pandas as pd
from prophet import Prophet
import json
from attribution_logic import get_zone_insight
from advisory import get_multilingual_advisory

def build_city_data(city_name, clean_csv, station_ids, min_aqi):
    # Load and forecast
    df = pd.read_csv(clean_csv)
    data = df[['Date', 'AQI']].rename(columns={'Date': 'ds', 'AQI': 'y'})
    data['ds'] = pd.to_datetime(data['ds'])

    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    forecast['yhat'] = forecast['yhat'].clip(lower=min_aqi)
    forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=min_aqi)
    forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=min_aqi)

    history = data.tail(90).copy()
    history['ds'] = history['ds'].dt.strftime('%Y-%m-%d')
    future_part = forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(30).copy()
    future_part['ds'] = pd.to_datetime(future_part['ds']).dt.strftime('%Y-%m-%d')

    current_aqi = float(data['y'].iloc[-1])
    tomorrow_aqi = float(future_part['yhat'].iloc[0])

    def aqi_category(val):
        if val <= 50: return "Good"
        elif val <= 100: return "Satisfactory"
        elif val <= 200: return "Moderate"
        elif val <= 300: return "Poor"
        elif val <= 400: return "Very Poor"
        else: return "Severe"

    zones = {}
    for sid in station_ids:
        zones[sid] = get_zone_insight(sid, city=city_name)

    advisory_result = get_multilingual_advisory(
        tomorrow_aqi, languages=['hi', 'ta', 'kn', 'pa']
    )

    return {
        "city": city_name,
        "current_aqi": round(current_aqi, 1),
        "current_category": aqi_category(current_aqi),
        "tomorrow_aqi": round(tomorrow_aqi, 1),
        "tomorrow_category": aqi_category(tomorrow_aqi),
        "advisory": advisory_result,
        "history": [{"date": r['ds'], "aqi": round(r['y'], 1)}
                    for _, r in history.iterrows()],
        "forecast": [{"date": r['ds'], "aqi": round(r['yhat'], 1),
                      "lower": round(r['yhat_lower'], 1),
                      "upper": round(r['yhat_upper'], 1)}
                     for _, r in future_part.iterrows()],
        "zones": zones
    }

# Build Delhi
print("Building Delhi...")
delhi_data = build_city_data(
    city_name='Delhi',
    clean_csv='delhi_clean.csv',
    station_ids=[
        'DL001','DL002','DL004','DL005','DL006','DL007','DL008','DL009',
        'DL010','DL011','DL012','DL013','DL014','DL015','DL016','DL017',
        'DL018','DL019','DL020','DL021','DL022','DL023','DL024','DL025',
        'DL026','DL027','DL028','DL029','DL030','DL031','DL032','DL033',
        'DL034','DL035','DL036','DL037','DL038'
    ],
    min_aqi=29
)
print(f"Delhi: current={delhi_data['current_aqi']}, tomorrow={delhi_data['tomorrow_aqi']}")

# Build Bengaluru
print("Building Bengaluru...")
bengaluru_data = build_city_data(
    city_name='Bengaluru',
    clean_csv='bengaluru_clean.csv',
    station_ids=['KA002','KA003','KA004','KA005','KA006','KA007','KA008','KA009','KA010','KA011'],
    min_aqi=20
)
print(f"Bengaluru: current={bengaluru_data['current_aqi']}, tomorrow={bengaluru_data['tomorrow_aqi']}")

# Save combined export
export = {
    "cities": {
        "Delhi": delhi_data,
        "Bengaluru": bengaluru_data
    }
}

with open('dashboard_data.json', 'w') as f:
    json.dump(export, f, indent=2)

print("\nExported dashboard_data.json successfully with both cities")