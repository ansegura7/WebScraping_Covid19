USE [DATABASE_NAME]
GO

/****** Object:  Table [dbo].[covid19_data]    Script Date: 4/13/2020 9:16:28 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[covid19_data](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[country] [nvarchar](100) NULL,
	[total_cases] [int] NULL,
	[total_deaths] [int] NULL,
	[total_recovered] [int] NULL,
	[active_cases] [int] NULL,
	[serious_critical] [int] NULL,
	[tot_cases_1m_pop] [float] NULL,
	[deaths_1m_pop] [float] NULL,
	[total_tests] [int] NULL,
	[tests_1m_pop] [float] NULL,
	[datestamp] [datetime] NULL,
 CONSTRAINT [PK_covid_19] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


