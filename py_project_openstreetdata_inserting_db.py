### Creating SQL Database
# Creating a database files from the newly created CSVs

import sqlite3
import csv
from pprint import pprint

sqlite_file = "udacity_project_openstreetdata_rjl/bozeman_MT.osm.db"

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

# Drop existing table from database if it already exists
cur.execute('''DROP TABLE IF EXISTS nodes''')
cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
cur.execute('''DROP TABLE IF EXISTS ways''')
cur.execute('''DROP TABLE IF EXISTS ways_tags''')
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')

conn.commit()

# Create new tables
cur.execute('''CREATE TABLE nodes(id INTEGER PRIMARY KEY NOT NULL, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT)''')
cur.execute('''CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES nodes (id))''')
cur.execute('''CREATE TABLE ways(id INTEGER PRIMARY KEY NOT NULL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT)''')
cur.execute('''CREATE TABLE ways_tags(id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, type TEXT, FOREIGN KEY (id) REFERENCES ways(id))''')cur.execute('''CREATE TABLE ways_nodes(id INTEGER NOT NULL, node_id INTEGER NOT NULL, position INTEGER NOT NULL, FOREIGN KEY (id) REFERENCES ways (id), FOREIGN KEY (node_id) REFERENCES nodes (id))''')

conn.commit()

# Insert the data from the nodes.csv file
with open('/Users/RichardJamesLopez/Dropbox/Jupyter/nodes.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_nodes = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_nodes)

conn.commit()
# The nodes data has been committed. <br/>
Now we can fetch some nodes data from the database and review how it looks
cur.execute('SELECT COUNT (*) FROM nodes')
cur.fetchall()

# Insert the data from the nodes_table.csv file
with open('/Users/RichardJamesLopez/Dropbox/Jupyter/nodes_tags.csv', 'rt') as f:
    d = csv.DictReader(f)
    to_nodes_tags = [(i['id'], i['key'], i['value'], i['type']) for i in d]

cur.executemany("INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_nodes_tags)

conn.commit()

# Checking for data insertion:
cur.execute("SELECT COUNT (*) FROM nodes_tags")
cur.fetchall()


# Insert the data from the ways.csv file
with open('/Users/RichardJamesLopez/Dropbox/Jupyter/ways.csv', 'rt') as g:
    r = csv.DictReader(g)
    to_ways = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in r]

cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_ways)

conn.commit()

# Checking for data insertion:
cur.execute("SELECT COUNT (*) FROM ways")
cur.fetchall()


# Insert the data from the ways_tags.csv file
with open('/Users/RichardJamesLopez/Dropbox/Jupyter/ways_tags.csv', 'rt') as h:
    s = csv.DictReader(h)
    to_ways_tags = [(i['id'], i['key'], i['value'], i['type']) for i in s]

cur.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_ways_tags)

conn.commit()

# Checking for data insertion:
cur.execute("SELECT COUNT (*) FROM ways_tags")
cur.fetchall()

# Insert the data from the ways_nodes.csv file
with open("/Users/RichardJamesLopez/Dropbox/Jupyter/ways_nodes.csv", "rt") as j:
    t = csv.DictReader(j)
    to_ways_nodes = [(i['id'], i['node_id'], i['position']) for i in t]

cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_ways_nodes)

conn.commit()

# Checking for data insertion:
cur.execute("SELECT COUNT (*) FROM ways_nodes")
cur.fetchall()

conn.close()

# Now the data has been committed to the database and we are free to explore the database,
# Next file is the preping the database file 'project_openstreetdata_chart.py'
