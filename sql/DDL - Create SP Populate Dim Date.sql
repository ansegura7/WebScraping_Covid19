USE [DATABASE_NAME]
GO

/****** Object:  StoredProcedure [dbo].[sp_populate_dim_date]    Script Date: 4/22/2020 2:22:08 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Andres Segura Tinoco
-- Create date: 04/21/2020
-- Description:	Stored procedure to populate the table dimension date
-- =============================================
CREATE PROCEDURE [dbo].[sp_populate_dim_date]
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here

	/********************************************************************************************/
	-- Specify Start Date and End date here
	-- Value of Start Date Must be Less than Your End Date 
	DECLARE @StartDate DATETIME = '01/01/2020';
	DECLARE @EndDate DATETIME = '01/01/2030';

	-- Temporary Variables To Hold the Values During Processing of Each Date of Year
	DECLARE
		@DayOfWeekInMonth INT,
		@DayOfWeekInYear INT,
		@DayOfQuarter INT,
		@WeekOfMonth INT,
		@CurrentYear INT,
		@CurrentMonth INT,
		@CurrentQuarter INT

	-- Table Data type to store the day of week count for the month and year
	DECLARE @DayOfWeek TABLE (DOW INT, MonthCount INT, QuarterCount INT, YearCount INT)
	INSERT INTO @DayOfWeek VALUES (1, 0, 0, 0)
	INSERT INTO @DayOfWeek VALUES (2, 0, 0, 0)
	INSERT INTO @DayOfWeek VALUES (3, 0, 0, 0)
	INSERT INTO @DayOfWeek VALUES (4, 0, 0, 0)
	INSERT INTO @DayOfWeek VALUES (5, 0, 0, 0)
	INSERT INTO @DayOfWeek VALUES (6, 0, 0, 0)
	INSERT INTO @DayOfWeek VALUES (7, 0, 0, 0)

	-- Extract and assign various parts of Values from Current Date to Variable
	DECLARE @CurrentDate AS DATETIME = @StartDate
	SET @CurrentMonth = DATEPART(MM, @CurrentDate)
	SET @CurrentYear = DATEPART(YY, @CurrentDate)
	SET @CurrentQuarter = DATEPART(QQ, @CurrentDate)

	/********************************************************************************************/
	-- Proceed only if Start Date(Current date ) is less than End date you specified above
	WHILE @CurrentDate < @EndDate
	BEGIN
		-- Begin day of week logic

		-- Check for Change in Month of the Current date if Month changed then Change variable value
		IF @CurrentMonth != DATEPART(MM, @CurrentDate) 
		BEGIN
			UPDATE @DayOfWeek
			SET MonthCount = 0
			SET @CurrentMonth = DATEPART(MM, @CurrentDate)
		END

		-- Check for Change in Quarter of the Current date if Quarter changed then change Variable value
		IF @CurrentQuarter != DATEPART(QQ, @CurrentDate)
		BEGIN
			UPDATE @DayOfWeek
			SET QuarterCount = 0
			SET @CurrentQuarter = DATEPART(QQ, @CurrentDate)
		END
       
		-- Check for Change in Year of the Current date if Year changed then change Variable value
		IF @CurrentYear != DATEPART(YY, @CurrentDate)
		BEGIN
			UPDATE @DayOfWeek
			SET YearCount = 0
			SET @CurrentYear = DATEPART(YY, @CurrentDate)
		END
	
		-- Set values in table data type created above from variables 
		UPDATE @DayOfWeek
		SET 
			MonthCount = MonthCount + 1,
			QuarterCount = QuarterCount + 1,
			YearCount = YearCount + 1
		WHERE DOW = DATEPART(DW, @CurrentDate)

		SELECT
			@DayOfWeekInMonth = MonthCount,
			@DayOfQuarter = QuarterCount,
			@DayOfWeekInYear = YearCount
		FROM @DayOfWeek
		WHERE DOW = DATEPART(DW, @CurrentDate)
		-- End day of week logic

		-- Populate Your Dimension Table with values
		INSERT INTO [dbo].[dim_date]
		SELECT
			CONVERT (char(8),@CurrentDate,112) AS date_key,
			@CurrentDate AS [date],
			CONVERT (char(10),@CurrentDate,101) AS full_date,
			DATEPART(DD, @CurrentDate) AS day_of_month,
			CASE 
				WHEN DATEPART(DD,@CurrentDate) IN (11,12,13) THEN CAST(DATEPART(DD,@CurrentDate) AS VARCHAR) + 'th'
				WHEN RIGHT(DATEPART(DD,@CurrentDate),1) = 1 THEN CAST(DATEPART(DD,@CurrentDate) AS VARCHAR) + 'st'
				WHEN RIGHT(DATEPART(DD,@CurrentDate),1) = 2 THEN CAST(DATEPART(DD,@CurrentDate) AS VARCHAR) + 'nd'
				WHEN RIGHT(DATEPART(DD,@CurrentDate),1) = 3 THEN CAST(DATEPART(DD,@CurrentDate) AS VARCHAR) + 'rd'
				ELSE CAST(DATEPART(DD,@CurrentDate) AS VARCHAR) + 'th' 
			END AS day_suffix,
			DATENAME(DW, @CurrentDate) AS day_name,
			DATEPART(DW, @CurrentDate) AS day_of_week,
			@DayOfWeekInMonth AS day_of_week_in_month,
			@DayOfWeekInYear AS day_of_week_in_year,
			@DayOfQuarter AS day_of_quarter,
			DATEPART(DY, @CurrentDate) AS day_of_year,
			DATEPART(WW, @CurrentDate) + 1 - DATEPART(WW, CONVERT(VARCHAR, DATEPART(MM, @CurrentDate)) + '/1/' + CONVERT(VARCHAR, DATEPART(YY, @CurrentDate))) AS week_of_month,
			(DATEDIFF(DD, DATEADD(QQ, DATEDIFF(QQ, 0, @CurrentDate), 0), @CurrentDate) / 7) + 1 AS week_of_quarter,
			DATEPART(WW, @CurrentDate) AS week_of_year,
			DATEPART(MM, @CurrentDate) AS [month],
			DATENAME(MM, @CurrentDate) AS month_name,
			CASE
				WHEN DATEPART(MM, @CurrentDate) IN (1, 4, 7, 10) THEN 1
				WHEN DATEPART(MM, @CurrentDate) IN (2, 5, 8, 11) THEN 2
				WHEN DATEPART(MM, @CurrentDate) IN (3, 6, 9, 12) THEN 3
			END AS month_of_quarter,
			DATEPART(QQ, @CurrentDate) AS [quarter],
			CASE DATEPART(QQ, @CurrentDate)
				WHEN 1 THEN 'First'
				WHEN 2 THEN 'Second'
				WHEN 3 THEN 'Third'
				WHEN 4 THEN 'Fourth'
			END AS quarter_name,
			DATEPART(YEAR, @CurrentDate) AS [year],
			'CY ' + CONVERT(VARCHAR, DATEPART(YEAR, @CurrentDate)) AS year_name,
			LEFT(DATENAME(MM, @CurrentDate), 3) + '-' + CONVERT(VARCHAR, DATEPART(YY, @CurrentDate)) AS month_year,
			RIGHT('0' + CONVERT(VARCHAR, DATEPART(MM, @CurrentDate)),2) + CONVERT(VARCHAR, DATEPART(YY, @CurrentDate)) AS [mm_yyyy],
			CONVERT(DATETIME, CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, @CurrentDate) - 1), @CurrentDate))) AS first_day_of_month,
			CONVERT(DATETIME, CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, @CurrentDate)))), DATEADD(MM, 1, @CurrentDate)))) AS last_day_of_month,
			DATEADD(QQ, DATEDIFF(QQ, 0, @CurrentDate), 0) AS first_day_of_quarter,
			DATEADD(QQ, DATEDIFF(QQ, -1, @CurrentDate), -1) AS last_day_of_quarter,
			CONVERT(DATETIME, '01/01/' + CONVERT(VARCHAR, DATEPART(YY, @CurrentDate))) AS first_day_of_year,
			CONVERT(DATETIME, '12/31/' + CONVERT(VARCHAR, DATEPART(YY, @CurrentDate))) AS last_day_of_year,
			CASE DATEPART(DW, @CurrentDate)
				WHEN 1 THEN 0
				WHEN 2 THEN 1
				WHEN 3 THEN 1
				WHEN 4 THEN 1
				WHEN 5 THEN 1
				WHEN 6 THEN 1
				WHEN 7 THEN 0
			END AS [is_weekday],
			NULL AS [is_holiday],
			NULL AS [holiday];

		SET @CurrentDate = DATEADD(DD, 1, @CurrentDate);
	END
	/********************************************************************************************/

END
GO
