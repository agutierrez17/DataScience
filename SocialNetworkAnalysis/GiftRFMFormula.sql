SELECT
[ID],

CASE 
WHEN [Lifetime Giving] < 1000 THEN 1 -- LESS THAN 1000
WHEN [Lifetime Giving] < 10000 THEN 2 -- LESS THAN 10000
WHEN [Lifetime Giving] < 100000 THEN 3 -- LESS THAN 100000
WHEN [Lifetime Giving] < 1000000 THEN 4 -- LESS THAN 1000000
WHEN [Lifetime Giving] < 5000000 THEN 5 -- LESS THAN 5000000
WHEN [Lifetime Giving] >= 5000000 THEN 6 -- 5000000+
END AS "Monetary Value Score",

CASE 
WHEN [Number of Gifts] = 1 THEN 1 
WHEN [Number of Gifts] < 3 THEN 2 
WHEN [Number of Gifts] < 5 THEN 3
WHEN [Number of Gifts] < 10 THEN 4
WHEN [Number of Gifts] < 20 THEN 5
WHEN [Number of Gifts] >= 20 THEN 6
END AS "Frequency Score",

CASE 
WHEN [Month Since Last Gift] < 12 THEN 6 -- LESS THAN ONE YEAR
WHEN [Month Since Last Gift] < 24 THEN 5 -- LESS THAN TWO YEARS
WHEN [Month Since Last Gift] < 36 THEN 4 -- LESS THAN THREE YEARS
WHEN [Month Since Last Gift] < 48 THEN 3 -- LESS THAN FOUR YEARS
WHEN [Month Since Last Gift] < 60 THEN 2 -- LESS THAN FIVE YEARS
WHEN [Month Since Last Gift] >= 60 THEN 1 -- GREATER THAN FIVE YEARS
END AS "Recency Score"

FROM [Philanthropy].[dbo].[GiftsRFMView]
