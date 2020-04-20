-- Temporal data
WITH [c19_data] AS (
	SELECT a.country, CAST(a.datestamp AS date) AS [datetime], a.total_cases, a.total_deaths, a.total_recovered,
		   a.active_cases, a.serious_critical, a.tot_cases_1m_pop, a.deaths_1m_pop, a.total_tests, a.tests_1m_pop
	  FROM [dbo].[covid19_data] AS a
	 INNER JOIN
		  (SELECT [country], YEAR([datestamp]) AS [year], MONTH([datestamp]) AS [month], DAY([datestamp]) AS [day],
				  MAX([datestamp]) AS [max_date]
			 FROM [dbo].[covid19_data]
			GROUP BY [country], YEAR([datestamp]), MONTH([datestamp]), DAY([datestamp])) AS b
		ON a.country = b.country
	   AND a.datestamp = b.max_date)

-- Evolution by country of C19 mortality
SELECT a.*
  FROM (
		SELECT ROW_NUMBER() OVER(PARTITION BY [datetime] ORDER BY total_deaths DESC) AS row_number, *
		  FROM [c19_data]) AS a
 WHERE a.[country] = 'Colombia'
 ORDER BY [datetime] ASC;