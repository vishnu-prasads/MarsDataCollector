from nasa_api import get_mars_weather, get_neo_data, get_earth_imagery
from data_processing import process_mars_weather, process_neo_data
from visualizations import plot_mars_temperature, plot_neo_scatter, plot_neo_histogram
import matplotlib.pyplot as plt

def main():
    # Mars Weather
    mars_data = get_mars_weather()
    mars_df = process_mars_weather(mars_data)
    plot_mars_temperature(mars_df)
    print("Mars temperature plot saved as 'mars_temperature.png'")

    # Near Earth Objects
    neo_data = get_neo_data()
    neo_df = process_neo_data(neo_data)
    plot_neo_scatter(neo_df)
    print("NEO scatter plot saved as 'neo_scatter.png'")
    plot_neo_histogram(neo_df)
    print("NEO histogram saved as 'neo_histogram.png'")

    # Earth Imagery
    # Note: This just saves the image, it doesn't create a plot
    earth_image = get_earth_imagery(29.78, -95.33, "2018-01-01")  # Example: Houston, TX
    with open("earth_image.png", "wb") as file:
        file.write(earth_image)
    print("Earth image saved as 'earth_image.png'")

if __name__ == "__main__":
    main()

