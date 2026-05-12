UPDATE R
SET R.[Recip Key] = R2.[Unique Key]
FROM dbo.Relationships R,
dbo.Relationships R2 
WHERE
R.[Recip Key] = 0
AND
R.ID = R2.[Related ID]
AND
R2.ID = R.[Related ID]
AND
R.Status = 'Confirmed'
AND
R2.Status = 'Confirmed'