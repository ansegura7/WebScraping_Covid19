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
SELECT dt.[country],[date],[datestamp],[total_cases],[total_deaths],[total_recovered],[active_cases],
	   [serious_critical],[tot_cases_1m_pop],[deaths_1m_pop],[total_tests],[tests_1m_pop]
  FROM 
	   (SELECT [country], CAST(a.[date] AS date) AS [date]
	      FROM [dbo].[dim_date] AS a
	     INNER JOIN
			   (SELECT [country], CAST(MIN(SWITCHOFFSET([datestamp], '+00:00')) AS date) AS [min_date], CAST(SWITCHOFFSET(SYSDATETIMEOFFSET(), '+00:00') AS date) AS [max_date]
				  FROM [dbo].[covid19_data]
				 GROUP BY [country]) AS b
			ON a.[date] BETWEEN b.min_date AND b.max_date) AS dd
  OUTER APPLY
	   (SELECT TOP 1 [country],[datestamp],[total_cases],[total_deaths],[total_recovered],[active_cases],[serious_critical],[tot_cases_1m_pop],[deaths_1m_pop],[total_tests],[tests_1m_pop]
		  FROM [dbo].[covid19_data] AS b
		 WHERE dd.[date] >= CAST(b.[datestamp] AS date)
		   AND dd.[country] = b.country
		 ORDER BY [datestamp] DESC) AS dt;
GO
