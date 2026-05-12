from faker import Faker
import pyodbc
import warnings
import pandas as pd
from random import shuffle, seed, randint, uniform
from datetime import date, datetime
from geopy.geocoders import Nominatim
import time
import json
import requests
import random_address

warnings.filterwarnings("ignore")

# Initialize Faker
fake = Faker(['en_US'])
fake.random.seed(4321)

# instantiate a new Nominatim client
app = Nominatim(user_agent="tutorial")

# Get latitude and longitude of address
def get_location_by_address(address):
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)

print(random_address.get_summary())
print(garbage)

# Get address by latitude and longitude
def get_location_by_latlong():
    while 1 == 1:
        latlong = fake.local_latlng()
        lat = latlong[0]
        long = latlong[1]
        new_address = app.reverse(lat + ', ' + long)
        new_address = str(new_address).split(", ")
        if new_address[0].isdigit() and len(new_address) == 7:
            break
    return new_address

# Generate random latitude
for i in range(1,200):
    lat = round(uniform(31,47), 6)
    long = round(uniform(-84,-122), 6)
    print(str(lat) + ', ' + str(long))
    new = app.reverse(str(lat) + ', ' + str(long))
    print(new)

print(garbage)


# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Query Address Info
print('Querying address data from database...')
print('')
sql = """
SELECT DISTINCT
[ID].ID,
E.[Address Line 1],
E.City,
E.State,
LEFT(E.ZIP,5) AS ZIP
FROM dbo.[Event Constituents] E
INNER JOIN dbo.[ID Crosswalk] ID ON E.[ID Number] = ID.[Orig ID]

UNION

SELECT DISTINCT
[ID].ID,
T.[Address Line 1],
T.City,
T.ST,
LEFT(T.ZIP,5) AS ZIP
FROM dbo.Transactions T
INNER JOIN dbo.[ID Crosswalk] ID ON T.[ID Number] = ID.[Orig ID]
"""
df = pd.read_sql(sql,conn)

# Iterate through list
rows = []
i = 1
for index, row in df.iterrows():
    # Pull down original data
    ID = row[0]
    address = row[1]
    city = row[2]
    ST = row[3]
    ZIP = row[4]
    
    # Generate new data
    new_address = get_location_by_latlong()
    try:
        street_number = new_address[0]
        address = new_address[1]
        city = new_address[2]
        County = new_address[3]
        ST = new_address[4]
        ZIP = new_address[5]
        Country = new_address[6]
    except Exception as e:
        print(e)
        print(new_address)
        print(garabege)
    
    # Collect and append
    row = (ID,street_number,address,city,County,ST,ZIP,Country)
    print(row)
    
    # Insert data into Addresses table
    print('Inserting row ' + str(i) + ' into Addresses table...')
    cursor.execute("""INSERT INTO [dbo].[Addresses_2] ([ID],[Street Number],[Address],[City],[County],[ST],[ZIP],[Country]) VALUES (?,?,?,?,?,?,?,?)""", row)
    cursor.commit()
    i += 1

### Truncate Addresses table
##cursor.execute("""TRUNCATE TABLE [dbo].[Addresses_2]""")
##cursor.commit()

print('All data inserted.')
print('')

cursor.close()
