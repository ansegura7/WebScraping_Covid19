-- Last record by country
SELECT a.id, a.total_cases, a.total_deaths, a.total_recovered, a.active_cases, a.serious_critical,
       a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tot_cases_1m_pop, CAST(a.datestamp AS date) AS [datetime]
  FROM [dbo].[covid19_data] AS a
 INNER JOIN
      (SELECT [country], YEAR([datestamp]) AS [year], MONTH([datestamp]) AS [month], DAY([datestamp]) AS [day]
			, MAX([datestamp]) AS [max_date]
		FROM [dbo].[covid19_data]
		GROUP BY [country], YEAR([datestamp]), MONTH([datestamp]), DAY([datestamp])) AS b
	ON a.country = b.country
   AND a.datestamp = b.max_date
 WHERE a.[country] = 'USA'
 ORDER BY a.datestamp DESC;
GO

-- Historical data by country
SELECT *
  FROM [dbo].[covid19_data]
 WHERE [country] = 'Colombia'
 ORDER BY [country], [datestamp] DESC;
GO
