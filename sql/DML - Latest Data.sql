-- Latest data by country sorted by total_deaths
SELECT ROW_NUMBER() OVER(ORDER BY total_deaths DESC) AS row_number, a.country, a.total_cases, a.total_deaths, a.total_recovered, 
	   a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop, a.datestamp
  FROM [dbo].[covid19_data] AS a
 WHERE a.[datestamp] = 
	(SELECT MAX(b.[datestamp])
	   FROM [dbo].[covid19_data] AS b
	  WHERE b.country = a.country);
GO

-- Percentage of deaths by country
SELECT ROW_NUMBER() OVER(ORDER BY total_deaths DESC) AS row_number, a.country, a.total_cases, a.total_deaths, a.total_recovered, 
	   a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop,
	   (CAST((1.0 * a.total_deaths / a.total_cases) AS float) * 100) AS [perc_death], a.datestamp
  FROM [dbo].[covid19_data] AS a
 WHERE a.[datestamp] = 
	(SELECT MAX(b.[datestamp])
	   FROM [dbo].[covid19_data] AS b
	  WHERE b.country = a.country)
   AND total_cases > 1000
 ORDER BY [perc_death] DESC;
GO

-- Countries with more reports
SELECT [country], COUNT(*) AS [count]
  FROM [dbo].[covid19_data]
 GROUP BY [country]
 ORDER BY [count] DESC;
GO
