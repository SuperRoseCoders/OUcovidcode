##dervmatplot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import psycopg2
import datetime
import numpy as np

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

# Create a 3D scatter plot (optional, if you want to plot the original data in 3D)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(dates, cases, deaths)
ax.set_xlabel("Date")
ax.set_ylabel("Cases")
ax.set_zlabel("Deaths")
ax.set_title("COVID-19 Cases and Deaths Over Time")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

# Calculate the derivative of cases and deaths data
diff_cases = np.diff(cases)
diff_deaths = np.diff(deaths)

# Plot the derivative data against the corresponding dates
plt.figure()
plt.plot(dates[1:], diff_cases, label="Cases Derivative")
plt.plot(dates[1:], diff_deaths, label="Deaths Derivative")
plt.xlabel("Date")
plt.ylabel("Derivative")
plt.title("Derivative of COVID-19 Cases and Deaths Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close the database connection
conn.close()
