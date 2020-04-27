USE [DATABASE_NAME]
GO

/****** Object:  View [dbo].[v_current_covid19_data]    Script Date: 4/26/2020 1:54:54 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Andres Segura Tinoco
-- Create date: 04/14/2020
-- Description:	Current covid 19 data view
-- =============================================
CREATE VIEW [dbo].[v_current_covid19_data]
AS
SELECT ROW_NUMBER() OVER(ORDER BY [total_deaths] DESC, [total_cases] DESC) AS [row_number], a.country, CAST(SWITCHOFFSET(SYSDATETIMEOFFSET(), '+00:00') AS date) AS [date], a.datestamp, 
	   a.total_cases, a.total_deaths, a.total_recovered, a.active_cases, a.serious_critical, a.total_tests, 
	   CAST((CASE WHEN ISNULL([total_cases], 0) > 0 THEN 1000000.0 * [total_cases] / [population] ELSE 0 END) AS numeric(9, 2)) AS [tot_cases_1m_pop],
	   CAST((CASE WHEN ISNULL([total_deaths], 0) > 0 THEN 1000000.0 * [total_deaths] / [population] ELSE 0 END) AS numeric(9, 2)) AS [deaths_1m_pop],
	   CAST((CASE WHEN ISNULL([total_tests], 0) > 0 THEN 1000000.0 * [total_tests] / [population] ELSE 0 END) AS numeric(9, 2)) AS [tests_1m_pop]
  FROM
	   (SELECT [name] AS [country], [population]
	      FROM [dbo].[country_info]) AS c
 INNER JOIN
	   [dbo].[covid19_data] AS a
	 ON c.[country] = a.[country]
 WHERE a.[datestamp] = 
		(SELECT MAX(b.[datestamp])
		   FROM [dbo].[covid19_data] AS b
		  WHERE b.country = a.country);
GO
