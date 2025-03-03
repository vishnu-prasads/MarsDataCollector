import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# NASA API key - replace with your own if you have one
API_KEY = "DEMO_KEY"

# NASA API endpoint for Mars weather data
URL = f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"

# Fetch data from NASA API
response = requests.get(URL)
data = response.json()

# Extract temperature data
sol_keys = data['sol_keys']
temperatures = [data[sol]['AT']['av'] for sol in sol_keys if 'AT' in data[sol]]

# Create a pandas DataFrame
df = pd.DataFrame({
    'Sol': sol_keys[:len(temperatures)],
    'Temperature': temperatures
})

# Convert Sol to datetime for better x-axis labeling
start_date = datetime.now().date() - timedelta(days=len(temperatures))
df['Date'] = [start_date + timedelta(days=i) for i in range(len(temperatures))]

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Temperature'], marker='o')

# Customize the plot
plt.title('Average Daily Temperature on Mars (Curiosity Rover)')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)

# Rotate and align the tick labels so they look better
plt.gcf().autofmt_xdate()

# Use a tight layout
plt.tight_layout()

# Show the plot
plt.show()

# Print the data
print(df)

