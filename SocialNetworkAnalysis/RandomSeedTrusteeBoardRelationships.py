import pyodbc
import warnings
import pandas as pd
from random import shuffle, seed, randint
from datetime import date, datetime
import time
import json
import requests

warnings.filterwarnings("ignore")

# Define organizations
orgs = ['The Aurora Starlight Foundation ',
'The Philanthropic Vision Institute ',
'The Community Catalyst Fund ',
'The Healthy Horizons Alliance ',
'The Environmental Stewardship Initiative ',
'The Educational Empowerment Trust ',
'The Cultural Exchange Council ',
'The Professional Network for Women ',
'The Humanitarian Disaster Relief Fund ',
'The International Aid Partnership ',
'The Social Impact Investment Fund ',
'The Equality Institute for Education ',
'The Sustainability Solutions Initiative ',
'The Children''s Welfare Foundation ',
'The Artistic Expression Trust ',
'The Scientific Discovery Society ',
'The Medical Research Alliance ',
'The Historical Preservation Society ',
'The Interfaith Cooperation Council ',
'The World Wildlife Conservancy Fund '
]

# Define relationship types and reciprocals
trustee = ['Serve as Trustee','Serve as Trustee']
board = ['Serve as Board Member','Serve as Board Member']
rel_types = [trustee,board]

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Randomly seed 1500 rows of employer relationships
print('Querying data from database...')
print('')
i = 0
while i < 1500:

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

    # Pick random organization
    rand_org = randint(0, 18)
    org = orgs[rand_org]
    
    # Pick random pair of relationships
    rand_rel = randint(0,1)
    rel = rel_types[rand_rel]
    rel_1 = rel[0]
    rel_2 = rel[1]

    # Prepare rows for insert
    rows = []
    row1 = (0,ID1,ID2,rel_1,'Confirmed',org)
    row2 = (0,ID2,ID1,rel_2,'Confirmed',org)
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
