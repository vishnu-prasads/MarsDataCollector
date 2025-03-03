import requests
from datetime import datetime, timedelta

API_KEY = "DEMO_KEY"  # Replace with your NASA API key

def get_mars_weather():
    url = f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"
    response = requests.get(url)
    return response.json()

def get_neo_data(days=7):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_earth_imagery(lat, lon, date):
    url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&date={date}&api_key={API_KEY}"
    response = requests.get(url)
    return response.content

