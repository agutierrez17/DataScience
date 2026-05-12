USE [Philanthropy]
GO

/****** Object:  View [dbo].[ConstituentsView]    Script Date: 4/1/2026 1:10:34 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



ALTER VIEW [dbo].[ConstituentsView] AS 

SELECT DISTINCT
----- DEMOGRAPHIC INFO
C.[ID],
C.[Last Name],
C.[First Name],
C.[Deceased],
C.[Birthdate],
DATEDIFF(HOUR,C.[Birthdate],GETDATE())/8766 AS Age,
C.Manager,

----- ADDRESS
A.[Address Line 1],
A.City,
A.ST,
A.ZIP,
'United States' AS Country,

----- GEOGRAPHIC INFO
Z.[Metro (CBSA)] AS "Metro Area",
CASE WHEN Z.[Metro (CBSA)] LIKE '% Micro Area%' THEN 'Micro Area' WHEN Z.[Metro (CBSA)] LIKE '% Metro Area%' THEN 'Metro Area' ELSE '' END AS "Geo Area Type",
Z.[ZIP Code Population] AS "ZIP Code Population",
M.[Households - Median income (dollars)] AS "Metro Median Income",
M.[Married-couple families - Median income (dollars)] AS "Metro Median Income (Married Families)",
M.[Married-couple families - Total] / M.[Households - Total] AS "Metro % of Households Married Families",


----- ALUMNI INFO
C.Alumnus,
C.School,
CASE WHEN C.Alumnus = 'Alumnus' THEN YEAR(DATEADD(YEAR,23,C.[Birthdate])) ELSE NULL END AS "GradYear",

----- GIVING INFO
COALESCE(SUM(G.[Amount]),0) AS "Lifetime Giving",
(SELECT MAX(G.[Gift Date]) FROM dbo.Gifts G WITH (NOLOCK) WHERE G.ID = C.ID) AS "Last Gift Date",
(SELECT SUM(G.[Amount]) FROM dbo.Gifts G WITH (NOLOCK) WHERE G.ID = C.ID AND G.[Gift Date] = (SELECT MAX(G.[Gift Date]) FROM dbo.Gifts G WITH (NOLOCK) WHERE G.ID = C.ID)) AS "Last Gift Amount",
(SELECT MAX(G.[Gift Type]) FROM dbo.Gifts G WITH (NOLOCK) WHERE G.ID = C.ID AND G.[Gift Date] = (SELECT MAX(G.[Gift Date]) FROM dbo.Gifts G WITH (NOLOCK) WHERE G.ID = C.ID)) AS "Last Gift Type",
(SELECT MAX(G.[Fund Name]) FROM dbo.GiftsView G WITH (NOLOCK) WHERE G.ID = C.ID AND G.[Gift Date] = (SELECT MAX(G.[Gift Date]) FROM dbo.Gifts G WITH (NOLOCK) WHERE G.ID = C.ID)) AS "Last Gift Fund",

----- EVENTS INFO
(SELECT COUNT(DISTINCT EA.[Event ID]) FROM dbo.Events E WITH (NOLOCK) INNER JOIN dbo.[Event Attendance] EA WITH (NOLOCK) ON E.[Event ID] = EA.[Event ID] AND EA.[Attendee Type] IN ('Registrants','Participants') AND E.[Event Status] IN ('Completed')  WHERE EA.ID = C.ID) AS "Events Attended",
(SELECT MAX(E.[Event Date]) FROM dbo.Events E WITH (NOLOCK) INNER JOIN dbo.[Event Attendance] EA WITH (NOLOCK) ON E.[Event ID] = EA.[Event ID] AND EA.[Attendee Type] IN ('Registrants','Participants') AND E.[Event Status] IN ('Completed')  WHERE EA.ID = C.ID) AS "Last Event Date",

------ SCORING
ISNULL(CASE 
WHEN RFM.[Lifetime Giving] < 1000 THEN 1 -- LESS THAN 1000
WHEN RFM.[Lifetime Giving] < 10000 THEN 2 -- LESS THAN 10000
WHEN RFM.[Lifetime Giving] < 100000 THEN 3 -- LESS THAN 100000
WHEN RFM.[Lifetime Giving] < 1000000 THEN 4 -- LESS THAN 1000000
WHEN RFM.[Lifetime Giving] < 5000000 THEN 5 -- LESS THAN 5000000
WHEN RFM.[Lifetime Giving] >= 5000000 THEN 6 -- 5000000+
END,0)
+
ISNULL(CASE 
WHEN RFM.[Number of Gifts] = 1 THEN 1 
WHEN RFM.[Number of Gifts] < 3 THEN 2 
WHEN RFM.[Number of Gifts] < 5 THEN 3
WHEN RFM.[Number of Gifts] < 10 THEN 4
WHEN RFM.[Number of Gifts] < 20 THEN 5
WHEN RFM.[Number of Gifts] >= 20 THEN 6
END,0) 
+
ISNULL(CASE 
WHEN RFM.[Month Since Last Gift] < 12 THEN 6 -- LESS THAN ONE YEAR
WHEN RFM.[Month Since Last Gift] < 24 THEN 5 -- LESS THAN TWO YEARS
WHEN RFM.[Month Since Last Gift] < 36 THEN 4 -- LESS THAN THREE YEARS
WHEN RFM.[Month Since Last Gift] < 48 THEN 3 -- LESS THAN FOUR YEARS
WHEN RFM.[Month Since Last Gift] < 60 THEN 2 -- LESS THAN FIVE YEARS
WHEN RFM.[Month Since Last Gift] >= 60 THEN 1 -- GREATER THAN FIVE YEARS
END,0) AS "Giving RFM Score",

ISNULL(CASE 
WHEN RFM.[Lifetime Giving] < 1000 THEN 1 -- LESS THAN 1000
WHEN RFM.[Lifetime Giving] < 10000 THEN 2 -- LESS THAN 10000
WHEN RFM.[Lifetime Giving] < 100000 THEN 3 -- LESS THAN 100000
WHEN RFM.[Lifetime Giving] < 1000000 THEN 4 -- LESS THAN 1000000
WHEN RFM.[Lifetime Giving] < 5000000 THEN 5 -- LESS THAN 5000000
WHEN RFM.[Lifetime Giving] >= 5000000 THEN 6 -- 5000000+
END,0) AS "Giving Monetary Score",

ISNULL(CASE 
WHEN RFM.[Number of Gifts] = 1 THEN 1 
WHEN RFM.[Number of Gifts] < 3 THEN 2 
WHEN RFM.[Number of Gifts] < 5 THEN 3
WHEN RFM.[Number of Gifts] < 10 THEN 4
WHEN RFM.[Number of Gifts] < 20 THEN 5
WHEN RFM.[Number of Gifts] >= 20 THEN 6
END,0) AS "Giving Frequency Score",

ISNULL(CASE 
WHEN RFM.[Month Since Last Gift] < 12 THEN 6 -- LESS THAN ONE YEAR
WHEN RFM.[Month Since Last Gift] < 24 THEN 5 -- LESS THAN TWO YEARS
WHEN RFM.[Month Since Last Gift] < 36 THEN 4 -- LESS THAN THREE YEARS
WHEN RFM.[Month Since Last Gift] < 48 THEN 3 -- LESS THAN FOUR YEARS
WHEN RFM.[Month Since Last Gift] < 60 THEN 2 -- LESS THAN FIVE YEARS
WHEN RFM.[Month Since Last Gift] >= 60 THEN 1 -- GREATER THAN FIVE YEARS
END,0) AS "Giving Recency Score"

FROM [Philanthropy].[dbo].[Constituents] C WITH (NOLOCK)
INNER JOIN dbo.Addresses A WITH (NOLOCK) ON C.ID = A.ID
INNER JOIN geo.ZIP_To_TownMetroState Z WITH (NOLOCK) ON Z.[ZIP Code] = A.ZIP AND Z.[USPS Default City for ZIP] = A.City
INNER JOIN geo.MetroAreaIncome M WITH (NOLOCK) ON Z.[CBSA Code] = M.[CBSA code]
LEFT OUTER JOIN dbo.GiftsView G WITH (NOLOCK) ON C.ID = G.ID
LEFT OUTER JOIN [dbo].[GiftsRFMView] RFM WITH (NOLOCK) ON C.ID = RFM.ID


GROUP BY
C.[ID],
C.[Last Name],
C.[First Name],
C.[Deceased],
C.[Birthdate],
DATEDIFF(HOUR,C.[Birthdate],GETDATE())/8766,
C.Alumnus,
C.School,
C.Manager,
A.[Address Line 1],
A.City,
A.ST,
A.ZIP,
Z.[Metro (CBSA)],
Z.[ZIP Code Population],
M.[Married-couple families - Total],
M.[Households - Total],
M.[Households - Median income (dollars)],
M.[Married-couple families - Median income (dollars)],
RFM.[Lifetime Giving],
RFM.[Number of Gifts],
RFM.[Month Since Last Gift]

GO


