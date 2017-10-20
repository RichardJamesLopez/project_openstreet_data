### project_openstreetmap_data_chart
import sqlite3
import csv
from pprint import pprint

# From previous file
sqlite_file = "udacity_project_openstreetdata_rjl/bozeman_MT.osm.db"

# connecting
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

# Still  have yet to count the amount of unique users that contributed to this file
unique_users = cur.execute("""SELECT COUNT(DISTINCT(e.uid))
                FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;""").fetchall()
pprint (unique_users)

# Now return to dissecting the data to search for venue types for possible visualization
cuisine_loc = cur.execute("""SELECT b.id, b.value, nodes.lat, nodes.lon
                             FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) b
                                   JOIN nodes ON b.id = nodes.id
                             WHERE b.key = 'cuisine'""").fetchall()
pprint(cuisine_loc)
len(cuisine_loc)

# Lets start to fetch the data for venue types in order to plot them together:
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# first ttest
plt.scatter([x[2] for x in cuisine_loc], [y[3] for y in cuisine_loc])

# Let's add some labels
plt.scatter([x[2] for x in cuisine_loc], [y[3] for y in cuisine_loc])
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Location of Resaturants in the Bozeman_MT area')

# For sizing parameters of plot:
# https://codeyarns.com/2014/10/27/how-to-change-size-of-matplotlib-plot/

fig_size = plt.rcParams["figure.figsize"]
fig_size

fig_size[0] = 12
fig_size[1] = 9
plt.rcParams['figure.figsize'] = fig_size

# Now the same for coffee shops: (but first let me get a count of the cafes)
cafe = cur.execute("""SELECT b.id, b.value, nodes.lat, nodes.lon
                             FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) b
                               JOIN nodes ON b.id = nodes.id
                             WHERE b.value = 'cafe'""").fetchall()
pprint (len(cafe))

# or using the same way that we counted the nodes and tags
cur.execute("""SELECT COUNT (*) FROM nodes_tags WHERE value = 'cafe'""")
cur.fetchall()

plt.scatter([x[2] for x in cafe], [y[3] for y in cafe], c='green')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Location of Cafes in the Bozeman_MT area')

# Bring them together
plt.scatter([x[2] for x in cuisine_loc], [y[3] for y in cuisine_loc], c='blue', label="Restaurants")
plt.scatter([x[2] for x in cafe], [y[3] for y in cafe], c='red', label="Cafes")
plt.xlabel('Latitude')
plt.ylabel('Longtitude')
plt.title('Restaurants and Cafes')
plt.legend(loc=2)

# Now for the ATMs:
atm = cur.execute("""SELECT b.id, b.value, nodes.lat, nodes.lon
                             FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) b
                               JOIN nodes ON b.id = nodes.id
                             WHERE b.value = 'atm'""").fetchall()

# Plot #3
plt.scatter([x[2] for x in atm], [y[3] for y in atm], c='red')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Location of ATMs in the Bozeman_MT area')

# Putting them all together, we get the following plot:
plt.scatter([x[2] for x in cuisine_loc], [y[3] for y in cuisine_loc], c='blue', label="Restaurants")
plt.scatter([x[2] for x in cafe], [y[3] for y in cafe], c='green', label="Cafes")
plt.scatter([x[2] for x in atm], [y[3] for y in atm], c='red', label="ATMs")
plt.xlabel('Latitude')
plt.ylabel('Longtitude')
plt.title('Restaurants, Cafes, ATMs')
plt.legend(loc=2)

# Close the db connection
conn.close()
