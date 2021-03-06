-- Latest data by country sorted by total_deaths
SELECT ROW_NUMBER() OVER(ORDER BY total_deaths DESC) AS row_number, a.country, a.datestamp, a.total_cases, a.total_deaths, a.total_recovered, 
	   a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop
  FROM [dbo].[v_current_covid19_data] AS a;
GO

-- Percentage of deaths by country
SELECT ROW_NUMBER() OVER(ORDER BY total_deaths DESC) AS row_number, a.country, a.datestamp, a.total_cases, a.total_deaths, a.total_recovered, 
	   a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop,
	   (CAST((1.0 * a.total_deaths / a.total_cases) AS float) * 100) AS [perc_death]
  FROM [dbo].[v_current_covid19_data] AS a
 WHERE total_cases > 1000
 ORDER BY [perc_death] DESC;
GO

-- Countries with more reports
SELECT [country], COUNT(*) AS [count], MIN([datestamp]) AS [min_data], MAX([datestamp]) AS [max_data]
  FROM [dbo].[covid19_data]
 GROUP BY [country]
 ORDER BY [count] DESC, [country];
GO

-- Countries with more daily data
SELECT [country], COUNT(*) AS [count], MIN([date]) AS [min_data], MAX([date]) AS [max_data]
  FROM [dbo].[v_daily_covid19_data]
 GROUP BY [country]
 ORDER BY [count] DESC, [country];
GO
