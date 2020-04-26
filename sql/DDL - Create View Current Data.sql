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
	   a.total_cases, a.total_deaths, a.total_recovered, a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop
  FROM [dbo].[covid19_data] AS a
 WHERE a.[datestamp] = 
		(SELECT MAX(b.[datestamp])
		   FROM [dbo].[covid19_data] AS b
		  WHERE b.country = a.country);
GO
