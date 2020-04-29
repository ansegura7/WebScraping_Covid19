USE [DATABASE_NAME]
GO

/****** Object:  View [dbo].[v_daily_covid19_data]    Script Date: 4/26/2020 2:26:50 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Andres Segura Tinoco
-- Create date: 04/18/2020
-- Description:	Daily covid 19 data view
-- =============================================
CREATE VIEW [dbo].[v_daily_covid19_data]
AS
SELECT dt.[country],[date],[datestamp],[total_cases],[total_deaths],[total_recovered],[active_cases],[serious_critical],[total_tests],
	   CAST((CASE WHEN ISNULL([total_cases], 0)  > 0 THEN 1000000.0 * [total_cases]  / [population] ELSE 0 END) AS numeric(9, 2)) AS [tot_cases_1m_pop],
	   CAST((CASE WHEN ISNULL([total_deaths], 0) > 0 THEN 1000000.0 * [total_deaths] / [population] ELSE 0 END) AS numeric(9, 2)) AS [deaths_1m_pop],
	   CAST((CASE WHEN ISNULL([total_tests], 0)  > 0 THEN 1000000.0 * [total_tests]  / [population] ELSE 0 END) AS numeric(9, 2)) AS [tests_1m_pop],
	   ([total_cases] - LAG([total_cases], 1)   OVER (PARTITION BY dt.[country] ORDER BY [datestamp])) AS [diff_total_cases],
	   ([total_deaths] - LAG([total_deaths], 1) OVER (PARTITION BY dt.[country] ORDER BY [datestamp])) AS [diff_total_deaths],
	   ([active_cases] - LAG([active_cases], 1) OVER (PARTITION BY dt.[country] ORDER BY [datestamp])) AS [diff_active_cases]
  FROM 
	   (SELECT [name] AS [country], [population]
	      FROM [dbo].[country_info]) AS tc
 INNER JOIN
	   (SELECT [country], CAST(a.[date] AS date) AS [date]
	      FROM [dbo].[dim_date] AS a
	     INNER JOIN
			   (SELECT [country], CAST(MIN(SWITCHOFFSET([datestamp], '+00:00')) AS date) AS [min_date], CAST(SWITCHOFFSET(SYSDATETIMEOFFSET(), '+00:00') AS date) AS [max_date]
				  FROM [dbo].[covid19_data]
				 GROUP BY [country]) AS b
			ON a.[date] BETWEEN b.min_date AND b.max_date) AS dd
	 ON tc.[country] = dd.[country]
  OUTER APPLY
	   (SELECT TOP 1 [country],[datestamp],[total_cases],[total_deaths],[total_recovered],[active_cases],[serious_critical],[total_tests]
		  FROM [dbo].[covid19_data] AS b
		 WHERE dd.[date] >= CAST(b.[datestamp] AS date)
		   AND dd.[country] = b.country
		 ORDER BY [datestamp] DESC) AS dt;
GO
