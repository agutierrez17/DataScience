SELECT DISTINCT
0,
R.ID,
R2.[Related ID],
'Coworker',
'Potential',
R.Notes
FROM dbo.Relationships R,
dbo.Relationships R2
WHERE
R.Status = 'Confirmed'
AND
R.[Recip Key] <> 0
AND
R2.Status = 'Confirmed'
AND
R2.[Recip Key] <> 0
AND
R.Notes = R2.Notes
AND
R.ID <> R2.ID
AND
R.ID <> R2.[Related ID]
AND
R.Notes = 'Neutrona Inc.'
AND
(R.ID = '104848779433' OR R2.[Related ID] = '104848779433')