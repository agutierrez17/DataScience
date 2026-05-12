import pyodbc
import warnings
import pandas as pd
from random import shuffle, seed, randint
from datetime import date, datetime
import time
import json
import requests

warnings.filterwarnings("ignore")

# Define companies
companies = ['GlobalTech Inc.','NovaCorp Industries''Finitech Solutions','Skylima Group','Valiant Innovations','QuantumX Enterprises','Prodigy Systems',
    'Neuroaid Technologies','Cyberia Holdings','Energine Inc.','Celestial Biotech','Hyperion Capital','Apexon Solutions','NovaStellar Ventures','ZenithTech Global',
    'Prospera Corp.','Helixus Group','QuantumLeap Technologies','Orionia Investments','Galaxia Enterprises','CosmosTech Solutions','NovaSpire Health',
    'Astralux Industries','Starlight Corp.','CelestialX Group','Galactic Ventures','Interstellar Tech','Neutrona Inc.','Orionstar Enterprises','StellarTech Solutions'
]

# Define relationship types and reciprocals
coworker = ['Coworker','Coworker']
boss_report = ['Boss','Direct Report']
rel_types = [coworker,boss_report]

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Randomly seed 3000 rows of employer relationships
print('Querying data from database...')
print('')
i = 0
while i < 3000:

    # Query first random ID for pair
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'

    ORDER BY
    NEWID()
    """)
    ID1 = cursor.fetchone()[0]

    # Query second random ID for pair
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    C.ID <> '%s'

    ORDER BY
    NEWID()
    """ % (ID1))
    ID2 = cursor.fetchone()[0]

    # Pick random company
    rand_com = randint(0, 28)
    company = companies[rand_com]
    
    # Pick random pair of relationships
    rand_rel = randint(0,1)
    rel = rel_types[rand_rel]
    rel_1 = rel[0]
    rel_2 = rel[1]

    # Prepare rows for insert
    rows = []
    row1 = (0,ID1,ID2,rel_1,'Confirmed',company)
    row2 = (0,ID2,ID1,rel_2,'Confirmed',company)
    rows.append(row1)
    rows.append(row2)

    # Insert data into Relationships table
    cursor.executemany("""INSERT INTO [dbo].[Relationships] ([Recip Key],[ID],[Related ID],[Relationship Type],[Status],[Notes]) VALUES (?,?,?,?,?,?)""", rows)
    cursor.commit()
    
    i += 1
    print(i)

print('All data inserted.')
print('')

cursor.close()
