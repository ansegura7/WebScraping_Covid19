USE [OVS_DEVOPS_WFS]
GO

-- Temporal daily data
WITH [c19_data] AS (
	SELECT [country], [total_cases], [total_deaths], ISNULL([total_recovered], 0) AS [total_recovered], [active_cases], ISNULL([serious_critical], 0) AS [serious_critical], 
		   ISNULL([tot_cases_1m_pop], 0) AS [tot_cases_1m_pop], ISNULL([deaths_1m_pop], 0) AS [deaths_1m_pop], ISNULL([total_tests], 0) AS [total_tests], 
		   ISNULL([tests_1m_pop], 0) AS [tests_1m_pop], [date], 
		   (CASE WHEN total_cases > 0 THEN 100.0 * total_deaths / total_cases ELSE 0 END) AS [perc_deaths],
		   (CASE WHEN total_tests > 0 THEN 100.0 * total_cases / total_tests ELSE 0 END) AS [perc_infection],
		   [region]
	  FROM [dbo].[v_daily_covid19_data] AS cd
	 INNER JOIN
	       [dbo].[country_info] AS ci
		ON cd.[country] = ci.[name]
)

-- Evolution by country of C19 mortality
SELECT [row_number], [country], [date], [total_deaths]
  FROM (
	SELECT *, ROW_NUMBER() OVER(PARTITION BY [date] ORDER BY [total_deaths] DESC) AS [row_number]
	  FROM [c19_data]) AS t
 WHERE [country] IN ('USA', 'Brazil', 'India', 'Mexico', 'UK', 'Italy', 'Peru', 'France', 'Spain', 'Iran', 'Belgium') --AND [date] = CAST(GETDATE() AS date)
 ORDER BY [date] ASC, [total_deaths] DESC;
GO
