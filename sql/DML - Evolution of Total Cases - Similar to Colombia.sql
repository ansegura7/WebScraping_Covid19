USE [OVS_DEVOPS_WFS]
GO
DECLARE @cols NVARCHAR(MAX)

WITH cte_data AS (
	SELECT [index], [country], [region], [flag], [total_cases] AS [value]
	  FROM 
		   (SELECT [country], [date], [total_cases],
			       --[total_deaths], SUM([total_cases]) OVER (PARTITION BY [country] ORDER BY [date]) AS [sum_cases], 
				   ROW_NUMBER() OVER (PARTITION BY [country] ORDER BY [date]) AS [index]
		      FROM [dbo].[v_daily_covid19_data]
			 WHERE [total_cases] > 0
		    ) AS cd
	 INNER JOIN
		   [country_info] AS ci
		ON cd.[country] = ci.[name]
)

SELECT * --[country], [69]
  FROM cte_data AS x
 PIVOT (
    MAX([value])
    FOR [index] IN ([1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],[29],[30],[31],[32],[33],[34],[35],[36],[37],[38],[39],[40],[41],[42],[43],[44],[45],[46],[47],[48],[49],[50],[51],[52],[53],[54],[55],[56],[57],[58],[59],[60],[61],[62],[63],[64],[65],[66],[67],[68],[69],[70],[71],[72],[73],[74],[75],[76],[77],[78],[79],[80])
	) AS p
 WHERE [country] IN ('Colombia', 'South Africa', 'Indonesia', 'Romania',  'Serbia', 'Ukraine', 'Denmark')
 ORDER BY [70] DESC;
GO

--SELECT @cols = COALESCE (@cols + ',[' + CAST([index] AS NVARCHAR) + ']', '[' + CAST([index] AS NVARCHAR) + ']')
--  FROM (SELECT DISTINCT [index] FROM cte_data) AS pv  
-- ORDER BY [index];

--SELECT @cols;