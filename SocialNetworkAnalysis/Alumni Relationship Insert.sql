INSERT INTO dbo.Relationships ([Recip Key],[ID],[Related ID],[Relationship Type],[Status],[Notes])
SELECT DISTINCT
0,
----- PROSPECT 1
C.ID,
--C.[Last Name],
--C.[First Name],
--C.[Alumnus],
--C.[School],
--C.[GradYear],
--C.[Lifetime Giving],
----- PROSPECT 2
C2.ID,
--C2.[Last Name],
--C2.[First Name],
--C2.[Alumnus],
--C2.[School],
--C2.[GradYear],
--C2.[Lifetime Giving]
'Classmate',
'Potential',
C.School + ', Class of ' + LTRIM(STR(C.GradYear))
FROM [Philanthropy].[dbo].[ConstituentsView] C
INNER JOIN [dbo].[ConstituentsView] C2 ON C.School = C2.School AND C.GradYear = C2.GradYear AND C.ID <> C2.ID AND C.GradYear IS NOT NULL

UPDATE R
SET R.[Recip Key] = R2.[Unique Key]
FROM [dbo].[Relationships] R 
INNER JOIN [dbo].[Relationships] R2 ON R.ID = R2.[Related ID] AND R.[Related ID] = R2.ID