import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import psycopg2
import numpy as np

# Function to fetch data from the "USACountry" table
def fetch_data_from_database():
    conn = psycopg2.connect(
        host="pixel.ourcloud.ou.edu",
        port=5432,
        database="panviz",
        user="panviz_readonly",
        password="T3u&c7U58V9H"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT "date", "cases", "deaths" FROM "USACountry"')
    results = cursor.fetchall()
    conn.close()
    return results

# Function to create the 3D scatter plot
def create_3d_scatter_plot(dates, cases, deaths):
    dates_numeric = mdates.date2num(dates)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_date(dates_numeric, cases, deaths, marker='o', linestyle='-', tz=None)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.set_zlabel("Deaths")
    ax.set_title("COVID-19 Cases and Deaths Over Time")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))  # Change the number of ticks as needed
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    return fig, ax

# Function to plot the derivative graph
def plot_derivative_graph(dates, cases, deaths):
    diff_cases = np.diff(cases)
    diff_deaths = np.diff(deaths)
    dates = mdates.num2date(mdates.date2num(dates))[1:]  # Convert only the derivative data
    plt.figure()
    plt.plot(dates, diff_cases, label="Cases Derivative")
    plt.plot(dates, diff_deaths, label="Deaths Derivative")
    plt.xlabel("Date")
    plt.ylabel("Derivative")
    plt.title("Derivative of COVID-19 Cases and Deaths Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

# Function to plot the FFT results
def plot_fft(data, label):
    fft_data = np.fft.fft(data)
    sampling_frequency = 1  # Assuming 1 day interval between data points
    frequencies = np.fft.fftfreq(len(data), d=sampling_frequency)
    plt.figure()
    plt.plot(frequencies, np.abs(fft_data), label=label)
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.title(f"FFT of {label}")
    plt.legend()
    plt.tight_layout()
    return plt

# Main function
def main():
    results = fetch_data_from_database()
    dates = [result[0] for result in results]
    cases = [result[1] for result in results]
    deaths = [result[2] for result in results]

    fig, ax = create_3d_scatter_plot(dates, cases, deaths)

    derivative_plot = plot_derivative_graph(dates, cases, deaths)

    cases_fft_plot = plot_fft(cases, label="Cases")
    deaths_fft_plot = plot_fft(deaths, label="Deaths")

    plt.show()

if __name__ == "__main__":
    main()