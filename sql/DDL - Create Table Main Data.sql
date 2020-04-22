USE [DATABASE_NAME]
GO

/****** Object:  Table [dbo].[covid19_data]    Script Date: 4/20/2020 8:56:25 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Andres Segura Tinoco
-- Create date: 04/09/2020
-- Description:	Main covid19 data
-- =============================================
CREATE TABLE [dbo].[covid19_data](
	[country] [nvarchar](100) NOT NULL,
	[datestamp] [datetime] NOT NULL,
	[total_cases] [int] NULL,
	[total_deaths] [int] NULL,
	[total_recovered] [int] NULL,
	[active_cases] [int] NULL,
	[serious_critical] [int] NULL,
	[tot_cases_1m_pop] [float] NULL,
	[deaths_1m_pop] [float] NULL,
	[total_tests] [int] NULL,
	[tests_1m_pop] [float] NULL,
 CONSTRAINT [PK_covid19_data] PRIMARY KEY CLUSTERED 
(
	[country] ASC,
	[datestamp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
