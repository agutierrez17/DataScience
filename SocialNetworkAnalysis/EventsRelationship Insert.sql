WITH CTE AS (
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

INSERT INTO dbo.Relationships ([Recip Key],[ID],[Related ID],[Relationship Type],[Status],[Notes])
SELECT DISTINCT
0,
EA.ID,
EA2.ID,
'Attended Event',
'Potential',
'Attended ' + E.[Event Name] + ' event in ' + E.[Event State] + ', ' + E.[Event Year]
FROM dbo.[Event Attendance] EA WITH (NOLOCK) 
INNER JOIN CTE ON EA.[Event ID] = CTE.[Event ID] AND EA.Participant = 'TRUE'
INNER JOIN dbo.Events E WITH (NOLOCK) ON E.[Event ID] = EA.[Event ID],

dbo.[Event Attendance] EA2 WITH (NOLOCK) 
INNER JOIN CTE CTE2 ON EA2.[Event ID] = CTE2.[Event ID] AND EA2.Participant = 'TRUE'

WHERE
EA.[Event ID] = EA2.[Event ID]
and
EA.ID <> EA2.ID


UPDATE R
SET R.[Recip Key] = R2.[Unique Key]
FROM [dbo].[Relationships] R 
INNER JOIN [dbo].[Relationships] R2 ON R.ID = R2.[Related ID] AND R2.ID = R.[Related ID]
WHERE
R.[Recip Key] = 0
AND
R.[Relationship Type] = 'Attended Event'
AND
R.Notes = R2.NOTES