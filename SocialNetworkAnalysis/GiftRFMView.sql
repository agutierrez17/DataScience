USE [Philanthropy]
GO

/****** Object:  View [dbo].[GiftsView]    Script Date: 3/27/2026 10:44:56 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[GiftsRFMView] AS

SELECT 
[ID],
SUM([Amount]) AS "Lifetime Giving",
COUNT(DISTINCT [Gift ID]) AS "Number of Gifts",
DATEDIFF(MONTH,MAX([Gift Date]),'2024-09-29') AS "Month Since Last Gift"

FROM [Philanthropy].[dbo].[Gifts] G WITH (NOLOCK)

GROUP BY
[ID]

GO


