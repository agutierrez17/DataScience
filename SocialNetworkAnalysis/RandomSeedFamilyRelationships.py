import pyodbc
import warnings
import pandas as pd
from random import shuffle, seed, randint
from datetime import date, datetime
import time
import json
import requests

warnings.filterwarnings("ignore")

# Define relationship types and reciprocals
spouse = ['Spouse','Spouse']
parent = ['Parent','Child']
grandparent = ['Grandparent','Grandchild']
sibling = ['Sibling','Sibling']
aunt_uncle = ['Aunt/Uncle','Niece/Nephew']
cousin = ['Cousin','Cousin']
in_law = ['Parent-in-law','Child-in-law']
rel_types = [parent,grandparent,sibling,aunt_uncle,cousin,in_law]

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Randomly seed 2000 rows of spouse-parent-child relationships
print('Inserting spouse-parent-child relationships...')
print('')
x = 0
while x < 2000:

    # Query random ID for first parent
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    R.ID IS NULL

    ORDER BY
    NEWID()
    """)
    ID1 = cursor.fetchone()[0]

    # Query second random ID for pair
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    C.ID <> '%s'
    AND
    R.ID IS NULL

    ORDER BY
    NEWID()
    """ % (ID1))
    ID2 = cursor.fetchone()[0]

    # Prepare rows for insert
    rows = []
    row1 = (0,ID1,ID2,'Spouse','Confirmed','')
    row2 = (0,ID2,ID1,'Spouse','Confirmed','')
    rows.append(row1)
    rows.append(row2)
    
    # Pick random number n of children
    rand_int = randint(0,3)

    # Pull n IDs for parent-child relationships
    IDs = []
    for i in range(0,rand_int):
        cursor.execute("""
        SELECT TOP 1
        C.ID
        FROM [Philanthropy].[dbo].[Constituents] C
	LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
        WHERE
        C.Deceased <> 'Y'
        AND
        C.[Alumnus] = 'Alumnus'
        AND
        C.ID NOT IN ('%s','%s')
	AND
	R.ID IS NULL

        ORDER BY
        NEWID()
        """ % (ID1,ID2))
        ID = cursor.fetchone()[0]
        row3 = (0,ID,ID1,'Child','Confirmed','')
        row4 = (0,ID1,ID,'Parent','Confirmed','')
        row5 = (0,ID,ID2,'Child','Confirmed','')
        row6 = (0,ID2,ID,'Parent','Confirmed','')
        rows.append(row3)
        rows.append(row4)
        rows.append(row5)
        rows.append(row6)
        IDs.append(ID)

    # Insert data into Relationships table
    cursor.executemany("""INSERT INTO [dbo].[Relationships] ([Recip Key],[ID],[Related ID],[Relationship Type],[Status],[Notes]) VALUES (?,?,?,?,?,?)""", rows)
    cursor.commit()
    
    x += 1
    print(x)

print('All data inserted.')
print('')


# Randomly seed 1000 rows of spouse-parent-child-grandparent relationships
print('Inserting grandparent-inlaw-spouse-parent-child-grandchild relationships...')
print('')
x = 0
while x < 1000:

    # Query random ID for first parent
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    R.ID IS NULL

    ORDER BY
    NEWID()
    """)
    ID1 = cursor.fetchone()[0]

    # Query second random ID for second parent
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    C.ID <> '%s'
    AND
    R.ID IS NULL

    ORDER BY
    NEWID()
    """ % (ID1))
    ID2 = cursor.fetchone()[0]

    # Prepare rows for insert
    rows = []
    row1 = (0,ID1,ID2,'Spouse','Confirmed','')
    row2 = (0,ID2,ID1,'Spouse','Confirmed','')
    rows.append(row1)
    rows.append(row2)

    # Query random ID for first grandparent
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    R.ID IS NULL
    AND
    C.ID NOT IN ('%s','%s')

    ORDER BY
    NEWID()
    """ % (ID1,ID2))
    ID3 = cursor.fetchone()[0]

    # Query second random ID for second grandparent
    cursor.execute("""
    SELECT TOP 1
    C.ID
    FROM [Philanthropy].[dbo].[Constituents] C
    LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
    WHERE
    C.Deceased <> 'Y'
    AND
    C.[Alumnus] = 'Alumnus'
    AND
    C.ID <> '%s'
    AND
    R.ID IS NULL
    AND
    C.ID NOT IN ('%s','%s')

    ORDER BY
    NEWID()
    """ % (ID3,ID1,ID2))
    ID4 = cursor.fetchone()[0]

    # Prepare rows for insert
    rows = []
    row1 = (0,ID3,ID4,'Spouse','Confirmed','')
    row2 = (0,ID4,ID3,'Spouse','Confirmed','')
    row3 = (0,ID3,ID1,'Parent','Confirmed','')
    row4 = (0,ID1,ID3,'Child','Confirmed','')
    row5 = (0,ID4,ID1,'Parent','Confirmed','')
    row6 = (0,ID1,ID4,'Child','Confirmed','')
    row7 = (0,ID3,ID2,'Parent-in-law','Confirmed','')
    row8 = (0,ID2,ID3,'Child-in-law','Confirmed','')
    row9 = (0,ID4,ID2,'Parent-in-law','Confirmed','')
    row10 = (0,ID2,ID4,'Child-in-law','Confirmed','')
    rows.append(row1)
    rows.append(row2)
    rows.append(row3)
    rows.append(row4)
    rows.append(row5)
    rows.append(row6)
    rows.append(row7)
    rows.append(row8)
    rows.append(row9)
    rows.append(row10)
    
    # Pick random number n of children
    rand_int = randint(0,3)

    # Pull n IDs for parent-child relationships
    IDs = []
    for i in range(0,rand_int):
        cursor.execute("""
        SELECT TOP 1
        C.ID
        FROM [Philanthropy].[dbo].[Constituents] C
	LEFT OUTER JOIN dbo.Relationships R ON C.ID = R.ID AND R.Status = 'Confirmed' AND R.[Relationship Type] IN ('Spouse','Parent','Child','Grandparent','Grandchild','Parent-in-law','Child-in-law')
        WHERE
        C.Deceased <> 'Y'
        AND
        C.[Alumnus] = 'Alumnus'
        AND
        C.ID NOT IN ('%s','%s')
	AND
	R.ID IS NULL

        ORDER BY
        NEWID()
        """ % (ID1,ID2))
        ID = cursor.fetchone()[0]
        row1 = (0,ID,ID1,'Child','Confirmed','')
        row2 = (0,ID1,ID,'Parent','Confirmed','')
        row3 = (0,ID,ID2,'Child','Confirmed','')
        row4 = (0,ID2,ID,'Parent','Confirmed','')
        row5 = (0,ID,ID3,'Grandchild','Confirmed','')
        row6 = (0,ID3,ID,'Grandparent','Confirmed','')
        row7 = (0,ID,ID4,'Granchild','Confirmed','')
        row8 = (0,ID4,ID,'Grandparent','Confirmed','')
        rows.append(row1)
        rows.append(row2)
        rows.append(row3)
        rows.append(row4)
        rows.append(row5)
        rows.append(row6)
        rows.append(row7)
        rows.append(row8)
        IDs.append(ID)


    # Insert data into Relationships table
    cursor.executemany("""INSERT INTO [dbo].[Relationships] ([Recip Key],[ID],[Related ID],[Relationship Type],[Status],[Notes]) VALUES (?,?,?,?,?,?)""", rows)
    cursor.commit()
    
    x += 1
    print(x)

print('All data inserted.')
print('')

cursor.close()
