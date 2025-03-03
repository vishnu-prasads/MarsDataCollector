import pandas as pd
from datetime import datetime, timedelta

def process_mars_weather(data):
    sol_keys = data['sol_keys']
    temperatures = [data[sol]['AT']['av'] for sol in sol_keys if 'AT' in data[sol]]
    
    df = pd.DataFrame({
        'Sol': sol_keys[:len(temperatures)],
        'Temperature': temperatures
    })
    
    start_date = datetime.now().date() - timedelta(days=len(temperatures))
    df['Date'] = [start_date + timedelta(days=i) for i in range(len(temperatures))]
    
    return df

def process_neo_data(data):
    neo_data = []
    for date, daily_data in data['near_earth_objects'].items():
        for neo in daily_data:
            neo_data.append({
                'Date': date,
                'ID': neo['id'],
                'Name': neo['name'],
                'Diameter': neo['estimated_diameter']['kilometers']['estimated_diameter_max'],
                'Hazardous': neo['is_potentially_hazardous_asteroid']
            })
    return pd.DataFrame(neo_data)

