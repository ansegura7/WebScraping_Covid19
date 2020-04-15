-- Last record by country
SELECT a.*
  FROM [dbo].[covid19_data] AS a
 INNER JOIN
      (SELECT [country], YEAR([datestamp]) AS [year], MONTH([datestamp]) AS [month], DAY([datestamp]) AS [day]
			, MAX([datestamp]) AS [max_date]
		FROM [dbo].[covid19_data]
		GROUP BY [country], YEAR([datestamp]), MONTH([datestamp]), DAY([datestamp])) AS b
	ON a.country = b.country
   AND a.datestamp = b.max_date
 WHERE a.[country] = 'Colombia'
 ORDER BY a.datestamp DESC;
GO

-- Historical data by country
SELECT *
  FROM [dbo].[covid19_data]
 WHERE [country] = 'Colombia'
 ORDER BY [country], [datestamp] DESC;
GO
