import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import psycopg2
import datetime


# Connect to the database
conn = psycopg2.connect(
    host="pixel.ourcloud.ou.edu",
    port=5432,
    database="panviz",
    user="panviz_readonly",
    password="T3u&c7U58V9H"
)

# Fetch the data from the "USACountry" table
cursor = conn.cursor()
cursor.execute('SELECT "date", "cases", "deaths" FROM "USACountry"')
results = cursor.fetchall()

# Prepare the data for plotting
dates = [result[0] for result in results]
cases = [result[1] for result in results]
deaths = [result[2] for result in results]

# Convert dates to Matplotlib's numeric format
dates = mdates.date2num(dates)

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(dates, cases, deaths)

# Set labels and formatting
ax.set_xlabel("Date")
ax.set_ylabel("Cases")
ax.set_zlabel("Deaths")
ax.set_title("COVID-19 Cases and Deaths Over Time")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Show monthly ticks
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Date format for x-axis

# Rotate x-axis labels for better readability
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

plt.tight_layout()
plt.show()

# Close the database connection
conn.close()