-- Historical data by country
SELECT a.country, CAST(a.datestamp AS date) AS [datetime], a.total_cases, a.total_deaths, a.total_recovered,
       a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop
  FROM [dbo].[covid19_data] AS a
 INNER JOIN
      (SELECT [country], YEAR([datestamp]) AS [year], MONTH([datestamp]) AS [month], DAY([datestamp]) AS [day],
			  MAX([datestamp]) AS [max_date]
		 FROM [dbo].[covid19_data]
		--WHERE datestamp < '2020-04-18 15:00'
		GROUP BY [country], YEAR([datestamp]), MONTH([datestamp]), DAY([datestamp])) AS b
	ON a.country = b.country
   AND a.datestamp = b.max_date
 ORDER BY a.country, a.datestamp DESC;
GO

-- Colombia historical data
SELECT a.country, CAST(a.datestamp AS date) AS [datetime], a.total_cases, a.total_deaths, a.total_recovered,
       a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop
  FROM [dbo].[covid19_data] AS a
 INNER JOIN
      (SELECT [country], YEAR([datestamp]) AS [year], MONTH([datestamp]) AS [month], DAY([datestamp]) AS [day],
			  MAX([datestamp]) AS [max_date]
		 FROM [dbo].[covid19_data]
		GROUP BY [country], YEAR([datestamp]), MONTH([datestamp]), DAY([datestamp])) AS b
	ON a.country = b.country
   AND a.datestamp = b.max_date
 WHERE a.[country] = 'Colombia'
 ORDER BY a.datestamp DESC;
GO

-- USA full data
SELECT *
  FROM [dbo].[covid19_data]
 WHERE [country] = 'USA'
 ORDER BY [country], [datestamp] DESC;
GO
