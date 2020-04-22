USE [DATABASE_NAME]
GO

/****** Object:  Table [dbo].[dim_date]    Script Date: 4/22/2020 1:57:01 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Andres Segura Tinoco
-- Create date: 04/21/2020
-- Description:	Table dimension date
-- =============================================
CREATE TABLE [dbo].[dim_date](
	[date_key] [int] NOT NULL,
	[date] [datetime] NULL,
	[full_date] [char](10) NULL,
	[day_of_month] [varchar](2) NULL,
	[day_suffix] [varchar](4) NULL,
	[day_name] [varchar](9) NULL,
	[day_of_week] [char](1) NULL,
	[day_of_week_in_month] [varchar](2) NULL,
	[day_of_week_in_year] [varchar](2) NULL,
	[day_of_quarter] [varchar](3) NULL,
	[day_of_year] [varchar](3) NULL,
	[week_of_month] [varchar](1) NULL,
	[week_of_quarter] [varchar](2) NULL,
	[week_of_year] [varchar](2) NULL,
	[month] [varchar](2) NULL,
	[month_name] [varchar](9) NULL,
	[month_of_quarter] [varchar](2) NULL,
	[quarter] [char](1) NULL,
	[quarter_name] [varchar](9) NULL,
	[year] [char](4) NULL,
	[year_name] [char](7) NULL,
	[month_year] [char](10) NULL,
	[mm_yyyy] [char](6) NULL,
	[first_day_of_month] [date] NULL,
	[last_day_of_month] [date] NULL,
	[first_day_of_quarter] [date] NULL,
	[last_day_of_quarter] [date] NULL,
	[first_day_of_year] [date] NULL,
	[last_day_of_year] [date] NULL,
	[is_weekday] [bit] NULL,
	[is_holiday] [bit] NULL,
	[holiday] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[date_key] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
