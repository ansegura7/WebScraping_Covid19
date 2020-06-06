USE [OVS_DEVOPS_WFS]
GO

WITH cte_data AS (
	SELECT [country], [date], [total_cases] AS [value]
	  FROM [dbo].[v_daily_covid19_data] AS cd
	 WHERE [date] IN ('2020-05-29', '2020-06-05')
)
-- Countries with total cases >= 5000 by Jun 05, 2020 
SELECT TOP 20 [country], [2020-05-29] AS [last_week], [2020-06-05] AS [curr_week],
	   (100.0 * ABS([2020-05-29] - [2020-06-05]) / [2020-05-29]) AS [perc_inc]
  FROM cte_data AS d
 PIVOT (
    MAX ([value])
    FOR [date] IN ([2020-05-29], [2020-06-05])
	) AS p
 WHERE [2020-06-05] > 5000 AND [2020-06-05] > [2020-05-29]
 ORDER BY [perc_inc] DESC;
GO

WITH cte_data AS (
	SELECT [country], [date], [total_deaths] AS [value]
	  FROM [dbo].[v_daily_covid19_data] AS cd
	 WHERE [date] IN ('2020-05-29', '2020-06-05')
)
-- Countries with total deaths >= 100 by Jun 05, 2020 
SELECT TOP 20 [country], [2020-05-29] AS [last_week], [2020-06-05] AS [curr_week],
	   (100.0 * ABS([2020-05-29] - [2020-06-05]) / [2020-05-29]) AS [perc_inc]
  FROM cte_data AS d
 PIVOT (
    MAX ([value])
    FOR [date] IN ([2020-05-29], [2020-06-05])
	) AS p
 WHERE [2020-06-05] > 100 AND [2020-06-05] > [2020-05-29]
 ORDER BY [perc_inc] DESC;
GO
