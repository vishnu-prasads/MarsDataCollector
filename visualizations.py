import matplotlib.pyplot as plt
import seaborn as sns

def plot_mars_temperature(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Temperature'], marker='o')
    plt.title('Average Daily Temperature on Mars (Curiosity Rover)')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig('mars_temperature.png')
    plt.close()

def plot_neo_scatter(df):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='Diameter', y='Date', hue='Hazardous', size='Diameter',
                    palette={True: 'red', False: 'green'}, sizes=(20, 200))
    plt.title('Near Earth Objects - Size and Potential Hazard')
    plt.xlabel('Estimated Max Diameter (km)')
    plt.ylabel('Date')
    plt.tight_layout()
    plt.savefig('neo_scatter.png')
    plt.close()

def plot_neo_histogram(df):
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='Diameter', hue='Hazardous', multiple='stack', palette={True: 'red', False: 'green'})
    plt.title('Distribution of Near Earth Object Sizes')
    plt.xlabel('Estimated Max Diameter (km)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('neo_histogram.png')
    plt.close()

