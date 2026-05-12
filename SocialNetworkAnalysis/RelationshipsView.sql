CREATE VIEW dbo.[RelationshipsView] AS

WITH Salon_Events AS (
SELECT
E.[Event ID]
FROM dbo.Events E
INNER JOIN dbo.[Event Attendance] EA ON E.[Event ID] = EA.[Event ID]

WHERE
E.[Event Status] = 'Completed'
AND
EA.Participant = 'TRUE'
AND
E.[Event Type] NOT IN ('Online Event')

GROUP BY
E.[Event ID]

HAVING
COUNT(*) < 20
)

---- CONFIRMED RELATIONSHIPS
SELECT 
[ID],
[Related ID],
[Relationship Type],
[Status],
[Notes]
FROM [Philanthropy].[dbo].[Relationships]
WHERE
[Status] = 'Confirmed'

UNION

---- ALUMNI CLASSMATES
SELECT DISTINCT
C.ID,
C2.ID,
'Classmate',
'Potential',
C.School + ', Class of ' + LTRIM(STR(C.GradYear))
FROM [Philanthropy].[dbo].[ConstituentsView] C
INNER JOIN [dbo].[ConstituentsView] C2 ON C.School = C2.School AND C.GradYear = C2.GradYear AND C.ID <> C2.ID AND C.GradYear IS NOT NULL

UNION

---- MUTUAL EVENT ATTENDANCE
SELECT DISTINCT
EA.ID,
EA2.ID,
'Attended Event',
'Potential',
'Attended ' + E.[Event Name] + ' event in ' + E.[Event State] + ', ' + E.[Event Year]
FROM dbo.[Event Attendance] EA WITH (NOLOCK) 
INNER JOIN Salon_Events  ON EA.[Event ID] = Salon_Events.[Event ID] AND EA.Participant = 'TRUE'
INNER JOIN dbo.Events E WITH (NOLOCK) ON E.[Event ID] = EA.[Event ID],

dbo.[Event Attendance] EA2 WITH (NOLOCK) 
INNER JOIN Salon_Events CTE2 ON EA2.[Event ID] = CTE2.[Event ID] AND EA2.Participant = 'TRUE'

WHERE
EA.[Event ID] = EA2.[Event ID]
and
EA.ID <> EA2.ID

GO