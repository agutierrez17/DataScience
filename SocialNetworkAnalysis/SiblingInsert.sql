INSERT INTO dbo.Relationships ([Recip Key],[ID],[Related ID],[Relationship Type],[Status],[Notes])
SELECT DISTINCT
0,
R.ID,
R3.ID,
'Sibling',
'Confirmed',
''
FROM dbo.Relationships R
INNER JOIN dbo.Relationships R2 ON R.ID = R2.[Related ID] AND R.[Related ID] = R2.ID AND R.[Relationship Type] = 'Child' AND R2.[Relationship Type] = 'Parent',

dbo.Relationships R3
INNER JOIN dbo.Relationships R4 ON R3.ID = R4.[Related ID] AND R3.[Related ID] = R4.ID AND R3.[Relationship Type] = 'Child' AND R4.[Relationship Type] = 'Parent'

WHERE
R3.ID <> R.ID
AND
R4.ID = R2.ID