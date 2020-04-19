-- Total stored data
SELECT COUNT(*) AS [count]
     , MAX([datestamp]) AS [last_record]
  FROM [dbo].[covid19_data];
GO

-- Countries with more cases
SELECT a.*
  FROM [dbo].[covid19_data] AS a
 WHERE [total_cases] = (SELECT MAX([total_cases])
					      FROM [dbo].[covid19_data]);
GO

-- Countries with more deaths
SELECT a.*
  FROM [dbo].[covid19_data] AS a
 WHERE [total_deaths] = (SELECT MAX([total_deaths])
					      FROM [dbo].[covid19_data]);
GO

-- Countries with more recovered people
SELECT a.*
  FROM [dbo].[covid19_data] AS a
 WHERE [total_recovered] = (SELECT MAX([total_recovered])
					          FROM [dbo].[covid19_data]);
GO

-- Countries with more deaths per one millon population
SELECT a.*
  FROM [dbo].[covid19_data] AS a
 WHERE [deaths_1m_pop] = (SELECT MAX([deaths_1m_pop])
					        FROM [dbo].[covid19_data]
						   WHERE [total_cases] > 1000);
GO

-- Countries with the highest death rate
SELECT a.*, (CAST((1.0 * [total_deaths] / [total_cases]) AS float) * 100) AS [perc_death]
  FROM [dbo].[covid19_data] AS a
 WHERE (CAST((1.0 * a.[total_deaths] / a.[total_cases]) AS float) * 100) = 
	(SELECT MAX(CAST((1.0 * [total_deaths] / [total_cases]) AS float) * 100)
	   FROM [dbo].[covid19_data] AS b
	  WHERE [total_cases] > 1000
	    AND [datestamp] = 
				(SELECT MAX(c.[datestamp])
				   FROM [dbo].[covid19_data] AS c
				  WHERE b.[country] = c.[country]));
GO