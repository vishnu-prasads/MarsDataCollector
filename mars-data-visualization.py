# Mars Data Visualization Project
# A Python project to extract and visualize Mars data from NASA APIs

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
from PIL import Image
from io import BytesIO

# Load environment variables (for API keys)
load_dotenv()

# NASA API key (get yours at https://api.nasa.gov/)
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")  # Uses DEMO_KEY if not set

class MarsDataCollector:
    def __init__(self, api_key=NASA_API_KEY):
        self.api_key = api_key
        
    def get_curiosity_photos(self, sol=1000, camera="FHAZ", page=1, per_page=10):
        """Fetch Mars Rover Curiosity photos based on sol (Mars day)"""
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
        params = {
            "sol": sol,
            "camera": camera,
            "page": page, 
            "per_page": per_page,
            "api_key": self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching Curiosity photos: {response.status_code}")
            return None
            
    def get_insight_weather(self):
        """Fetch weather data from InSight Mars lander"""
        # Note: InSight stopped returning weather data in 2021, but we'll
        # demonstrate how to access this data anyway as an example
        url = f"https://api.nasa.gov/insight_weather/?api_key={self.api_key}&feedtype=json&ver=1.0"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching InSight weather: {response.status_code}")
            print("Note: InSight weather data service is discontinued as of 2021.")
            # Return some sample data for demonstration
            return self._get_sample_insight_data()
            
    def _get_sample_insight_data(self):
        """Return sample InSight data for demonstration purposes"""
        return {
            "sol_keys": ["1000", "1001", "1002", "1003", "1004", "1005", "1006"],
            "1000": {
                "AT": {"av": -76.0, "mn": -101.0, "mx": -28.0},
                "PRE": {"av": 750.0, "mn": 740.0, "mx": 780.0},
                "HWS": {"av": 5.0, "mn": 0.2, "mx": 15.0}
            },
            "1001": {
                "AT": {"av": -72.0, "mn": -98.0, "mx": -25.0},
                "PRE": {"av": 755.0, "mn": 743.0, "mx": 778.0},
                "HWS": {"av": 5.5, "mn": 0.5, "mx": 16.0}
            },
            "1002": {
                "AT": {"av": -74.0, "mn": -99.0, "mx": -27.0},
                "PRE": {"av": 752.0, "mn": 741.0, "mx": 777.0},
                "HWS": {"av": 6.0, "mn": 0.7, "mx": 17.0}
            },
            "1003": {
                "AT": {"av": -75.0, "mn": -100.0, "mx": -29.0},
                "PRE": {"av": 753.0, "mn": 742.0, "mx": 776.0},
                "HWS": {"av": 4.5, "mn": 0.3, "mx": 14.0}
            },
            "1004": {
                "AT": {"av": -77.0, "mn": -102.0, "mx": -30.0},
                "PRE": {"av": 751.0, "mn": 740.0, "mx": 775.0},
                "HWS": {"av": 4.0, "mn": 0.2, "mx": 13.0}
            },
            "1005": {
                "AT": {"av": -73.0, "mn": -99.0, "mx": -26.0},
                "PRE": {"av": 749.0, "mn": 737.0, "mx": 772.0},
                "HWS": {"av": 5.2, "mn": 0.4, "mx": 15.5}
            },
            "1006": {
                "AT": {"av": -71.0, "mn": -97.0, "mx": -24.0},
                "PRE": {"av": 748.0, "mn": 736.0, "mx": 770.0},
                "HWS": {"av": 6.2, "mn": 0.8, "mx": 16.8}
            }
        }
            
    def get_mars_rover_mission_data(self):
        """Get overall mission data for all Mars rovers"""
        url = "https://api.nasa.gov/mars-photos/api/v1/rovers"
        params = {"api_key": self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching rover mission data: {response.status_code}")
            return None
    
    def get_mars_epic_imagery(self):
        """Get EPIC (Earth Polychromatic Imaging Camera) imagery of Mars"""
        # Note: EPIC is for Earth imagery, not Mars. For demonstration purposes, 
        # we'll use the Mars APOD (Astronomy Picture of the Day) data instead.
        url = "https://api.nasa.gov/planetary/apod"
        params = {
            "api_key": self.api_key,
            "count": 10,
            "thumbs": True
        }
        
        response = requests.get(url, params=params)
        mars_images = []
        
        if response.status_code == 200:
            all_images = response.json()
            # Filter for Mars-related images
            for image in all_images:
                if "mars" in image.get("title", "").lower() or "mars" in image.get("explanation", "").lower():
                    mars_images.append(image)
            
            return mars_images if mars_images else all_images[:3]  # Return at least some images
        else:
            print(f"Error fetching APOD images: {response.status_code}")
            return None
    
    def get_mars_assets(self):
        """Get Mars imagery from NASA Earth Observations assets"""
        # This is simulated for demonstration purposes
        # In a real application, you might use the NASA imagery APIs
        return {
            "assets": [
                {"name": "Olympus Mons", "height": 21.9, "diameter": 600},
                {"name": "Valles Marineris", "length": 4000, "depth": 7},
                {"name": "Gale Crater", "diameter": 154, "depth": 5.5},
                {"name": "Jezero Crater", "diameter": 49, "depth": 2.5},
                {"name": "Syrtis Major", "diameter": 1500, "type": "volcanic plain"},
                {"name": "Hellas Planitia", "diameter": 2300, "depth": 7.2},
                {"name": "Utopia Planitia", "diameter": 3300, "depth": 1.5}
            ]
        }


class MarsDataAnalyzer:
    def __init__(self, collector):
        self.collector = collector
        
    def analyze_rover_mission_data(self):
        """Analyze rover mission data and return a pandas DataFrame"""
        mission_data = self.collector.get_mars_rover_mission_data()
        
        if not mission_data or "rovers" not in mission_data:
            print("No rover mission data available.")
            return None
            
        rovers = []
        for rover in mission_data["rovers"]:
            rover_info = {
                "name": rover["name"],
                "landing_date": rover["landing_date"],
                "launch_date": rover["launch_date"],
                "status": rover["status"],
                "max_sol": rover["max_sol"],
                "total_photos": rover["total_photos"],
                "cameras": len(rover["cameras"])
            }
            rovers.append(rover_info)
            
        return pd.DataFrame(rovers)
        
    def analyze_insight_weather(self):
        """Analyze InSight weather data and return DataFrames for temperature, pressure, and wind"""
        weather_data = self.collector.get_insight_weather()
        
        if not weather_data or "sol_keys" not in weather_data:
            print("No InSight weather data available.")
            return None, None, None
            
        sol_keys = weather_data["sol_keys"]
        
        # Initialize lists to store data
        temps = []
        pressures = []
        winds = []
        
        for sol in sol_keys:
            sol_data = weather_data[sol]
            
            # Temperature data (AT = Atmospheric Temperature)
            if "AT" in sol_data:
                temps.append({
                    "sol": int(sol),
                    "average": sol_data["AT"]["av"],
                    "min": sol_data["AT"]["mn"],
                    "max": sol_data["AT"]["mx"]
                })
                
            # Pressure data (PRE = Pressure)
            if "PRE" in sol_data:
                pressures.append({
                    "sol": int(sol),
                    "average": sol_data["PRE"]["av"],
                    "min": sol_data["PRE"]["mn"],
                    "max": sol_data["PRE"]["mx"]
                })
                
            # Wind data (HWS = Horizontal Wind Speed)
            if "HWS" in sol_data:
                winds.append({
                    "sol": int(sol),
                    "average": sol_data["HWS"]["av"],
                    "min": sol_data["HWS"]["mn"],
                    "max": sol_data["HWS"]["mx"]
                })
                
        # Convert to DataFrames
        temp_df = pd.DataFrame(temps) if temps else None
        pressure_df = pd.DataFrame(pressures) if pressures else None
        wind_df = pd.DataFrame(winds) if winds else None
        
        return temp_df, pressure_df, wind_df
        
    def analyze_mars_assets(self):
        """Analyze Mars geographic assets data"""
        assets_data = self.collector.get_mars_assets()
        
        if not assets_data or "assets" not in assets_data:
            print("No Mars assets data available.")
            return None
            
        return pd.DataFrame(assets_data["assets"])
        
    def analyze_rover_photo_metadata(self):
        """Analyze metadata from rover photos"""
        # Get photos from different cameras and sols for diversity
        cameras = ["FHAZ", "RHAZ", "NAVCAM", "MAST"]
        sols = [1000, 2000, 3000]
        
        all_photos = []
        
        for sol in sols:
            for camera in cameras:
                photos = self.collector.get_curiosity_photos(sol=sol, camera=camera, per_page=5)
                if photos and "photos" in photos and photos["photos"]:
                    for photo in photos["photos"]:
                        photo_info = {
                            "id": photo["id"],
                            "sol": photo["sol"],
                            "camera": photo["camera"]["name"],
                            "earth_date": photo["earth_date"],
                            "rover": photo["rover"]["name"],
                            "rover_status": photo["rover"]["status"]
                        }
                        all_photos.append(photo_info)
        
        if not all_photos:
            print("No photo metadata available.")
            return None
            
        return pd.DataFrame(all_photos)


class MarsDataVisualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        # Set up a consistent style for visualizations
        sns.set_style("darkgrid")
        plt.rcParams["figure.figsize"] = (12, 8)
        plt.rcParams["font.size"] = 12
        
    def visualize_rover_mission_data(self, save_path="rover_mission_comparison.png"):
        """Create a visualization comparing key metrics across rovers"""
        df = self.analyzer.analyze_rover_mission_data()
        
        if df is None or df.empty:
            print("No rover mission data to visualize.")
            return
        
        # Create a figure with multiple subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("Mars Rover Mission Comparison", fontsize=20)
        
        # Plot 1: Total photos by rover (bar chart)
        df.plot(kind="bar", x="name", y="total_photos", ax=axes[0, 0], 
                color="orangered", legend=False)
        axes[0, 0].set_title("Total Photos Taken")
        axes[0, 0].set_ylabel("Number of Photos")
        axes[0, 0].set_xlabel("")
        
        # Plot 2: Max sols by rover (bar chart)
        df.plot(kind="bar", x="name", y="max_sol", ax=axes[0, 1], 
                color="firebrick", legend=False)
        axes[0, 1].set_title("Mission Duration (Sols)")
        axes[0, 1].set_ylabel("Sols")
        axes[0, 1].set_xlabel("")
        
        # Plot 3: Camera count by rover (bar chart)
        df.plot(kind="bar", x="name", y="cameras", ax=axes[1, 0], 
                color="darkred", legend=False)
        axes[1, 0].set_title("Number of Cameras")
        axes[1, 0].set_ylabel("Camera Count")
        axes[1, 0].set_xlabel("")
        
        # Plot 4: Rover status (pie chart)
        status_counts = df["status"].value_counts()
        status_colors = ["green" if status == "active" else "gray" for status in status_counts.index]
        status_counts.plot(kind="pie", ax=axes[1, 1], autopct='%1.1f%%', 
                          colors=status_colors, startangle=90)
        axes[1, 1].set_title("Rover Status")
        axes[1, 1].set_ylabel("")
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.savefig(save_path)
        plt.close()
        
        print(f"Rover mission visualization saved to {save_path}")
        
    def visualize_insight_weather(self, save_path="mars_weather.png"):
        """Create visualizations of InSight weather data"""
        temp_df, pressure_df, wind_df = self.analyzer.analyze_insight_weather()
        
        if temp_df is None or pressure_df is None or wind_df is None:
            print("No InSight weather data to visualize.")
            return
            
        fig, axes = plt.subplots(3, 1, figsize=(14, 16))
        fig.suptitle("Mars Weather from InSight Lander", fontsize=22)
        
        # Mars-like colors
        mars_red = "#c1440e"
        mars_dark = "#5c2626"
        mars_orange = "#d3825f"
        
        # Temperature plot (line chart with min/max range)
        axes[0].plot(temp_df["sol"], temp_df["average"], marker="o", 
                    linestyle="-", color=mars_red, label="Average Temp (°C)")
        axes[0].fill_between(temp_df["sol"], temp_df["min"], temp_df["max"], 
                            alpha=0.3, color=mars_orange, label="Min-Max Range")
        axes[0].set_title("Temperature Variations (°C)", fontsize=16)
        axes[0].set_xlabel("Sol (Mars Day)")
        axes[0].set_ylabel("Temperature (°C)")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Pressure plot (line chart)
        axes[1].plot(pressure_df["sol"], pressure_df["average"], marker="s", 
                   linestyle="-", color=mars_dark, label="Average Pressure (Pa)")
        axes[1].fill_between(pressure_df["sol"], pressure_df["min"], pressure_df["max"], 
                           alpha=0.3, color=mars_orange, label="Min-Max Range")
        axes[1].set_title("Atmospheric Pressure Variations (Pa)", fontsize=16)
        axes[1].set_xlabel("Sol (Mars Day)")
        axes[1].set_ylabel("Pressure (Pa)")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Wind speed plot (bar chart with error bars)
        axes[2].bar(wind_df["sol"], wind_df["average"], color=mars_orange, 
                  yerr=[wind_df["average"]-wind_df["min"], wind_df["max"]-wind_df["average"]], 
                  capsize=5, label="Average Wind Speed (m/s)")
        axes[2].set_title("Wind Speed Variations (m/s)", fontsize=16)
        axes[2].set_xlabel("Sol (Mars Day)")
        axes[2].set_ylabel("Wind Speed (m/s)")
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        plt.savefig(save_path)
        plt.close()
        
        print(f"Mars weather visualization saved to {save_path}")
        
    def visualize_mars_assets(self, save_path="mars_features.png"):
        """Visualize Mars geographic features/assets"""
        df = self.analyzer.analyze_mars_assets()
        
        if df is None or df.empty:
            print("No Mars assets data to visualize.")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle("Notable Mars Geographic Features", fontsize=20)
        
        # Create custom Mars-like colormap
        mars_colors = ["#c1440e", "#d97b6c", "#a9331c", "#5c2626", "#d3825f"]
        mars_cmap = ListedColormap(mars_colors)
        
        # Plot 1: Feature sizes (bubble chart)
        if "diameter" in df.columns:
            scatter = axes[0].scatter(df.index, df["diameter"], 
                           s=df["diameter"]*5, # Size bubbles based on diameter
                           c=range(len(df)), cmap=mars_cmap,
                           alpha=0.7)
            
            # Add feature names as annotations
            for i, name in enumerate(df["name"]):
                axes[0].annotate(name, (i, df["diameter"].iloc[i]), 
                                fontsize=9, ha='center')
                
            axes[0].set_title("Geographic Feature Size Comparison")
            axes[0].set_ylabel("Diameter (km)")
            axes[0].set_xlabel("Feature Index")
            axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Feature depths where available (bar chart)
        if "depth" in df.columns:
            depth_data = df.dropna(subset=["depth"])
            bars = axes[1].bar(depth_data["name"], depth_data["depth"], 
                             color=mars_colors[:len(depth_data)])
            
            axes[1].set_title("Depth of Mars Features")
            axes[1].set_ylabel("Depth (km)")
            axes[1].set_xlabel("Feature Name")
            axes[1].set_xticklabels(depth_data["name"], rotation=45, ha="right")
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.savefig(save_path)
        plt.close()
        
        print(f"Mars geographic features visualization saved to {save_path}")
        
    def visualize_rover_photo_metadata(self, save_path="rover_photos_analysis.png"):
        """Visualize analysis of Mars rover photo metadata"""
        df = self.analyzer.analyze_rover_photo_metadata()
        
        if df is None or df.empty:
            print("No rover photo metadata to visualize.")
            return
            
        # Convert earth_date to datetime
        df["earth_date"] = pd.to_datetime(df["earth_date"])
            
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("Mars Rover Photography Analysis", fontsize=20)
        
        # Plot 1: Photos by camera type (pie chart)
        camera_counts = df["camera"].value_counts()
        camera_counts.plot(kind="pie", ax=axes[0, 0], autopct='%1.1f%%', 
                         cmap="OrRd", startangle=90)
        axes[0, 0].set_title("Photos by Camera Type")
        axes[0, 0].set_ylabel("")
        
        # Plot 2: Photos over time (line chart)
        time_data = df.groupby(df["earth_date"].dt.to_period("M")).size()
        time_data.index = time_data.index.to_timestamp()
        time_data.plot(kind="line", ax=axes[0, 1], marker="o", color="#c1440e")
        axes[0, 1].set_title("Photo Count Over Time")
        axes[0, 1].set_ylabel("Number of Photos")
        axes[0, 1].set_xlabel("Earth Date")
        
        # Plot 3: Photos by sol (histogram)
        df["sol"].plot(kind="hist", ax=axes[1, 0], bins=20, color="#a9331c")
        axes[1, 0].set_title("Distribution of Photos by Sol")
        axes[1, 0].set_ylabel("Count")
        axes[1, 0].set_xlabel("Sol")
        
        # Plot 4: Photos by rover (bar chart)
        rover_counts = df["rover"].value_counts()
        rover_counts.plot(kind="bar", ax=axes[1, 1], color="#d3825f")
        axes[1, 1].set_title("Photos by Rover")
        axes[1, 1].set_ylabel("Number of Photos")
        axes[1, 1].set_xlabel("Rover")
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.savefig(save_path)
        plt.close()
        
        print(f"Rover photo metadata visualization saved to {save_path}")


def run_mars_data_project():
    """Main function to run the Mars data project"""
    print("Starting Mars Data Visualization Project...")
    
    # Create collector, analyzer, and visualizer objects
    collector = MarsDataCollector()
    analyzer = MarsDataAnalyzer(collector)
    visualizer = MarsDataVisualizer(analyzer)
    
    # Create output directory if it doesn't exist
    output_dir = "mars_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Generate all visualizations
    print("\nGenerating visualizations...")
    visualizer.visualize_rover_mission_data(os.path.join(output_dir, "rover_mission_comparison.png"))
    visualizer.visualize_insight_weather(os.path.join(output_dir, "mars_weather.png"))
    visualizer.visualize_mars_assets(os.path.join(output_dir, "mars_features.png"))
    visualizer.visualize_rover_photo_metadata(os.path.join(output_dir, "rover_photos_analysis.png"))
    
    print("\nMars Data Visualization Project completed!")
    print(f"All visualizations saved to the '{output_dir}' directory.")


if __name__ == "__main__":
    run_mars_data_project()
