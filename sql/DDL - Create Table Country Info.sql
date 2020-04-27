USE [DATABASE_NAME]
GO

/****** Object:  Table [dbo].[country_info]    Script Date: 4/27/2020 1:48:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Andres Segura Tinoco
-- Create date: 04/27/2020
-- Description:	Master table of countries
-- =============================================
CREATE TABLE [dbo].[country_info](
	[name] [nvarchar](100) NOT NULL,
	[fullname] [nvarchar](100) NULL,
	[top_level_domain] [nvarchar](100) NULL,
	[alpha2_dode] [nvarchar](50) NULL,
	[alpha3_code] [nvarchar](50) NULL,
	[calling_codes] [nvarchar](50) NULL,
	[capital] [nvarchar](100) NULL,
	[alt_spellings] [nvarchar](250) NULL,
	[region] [nvarchar](50) NULL,
	[subregion] [nvarchar](50) NULL,
	[population] [int] NULL,
	[lat] [float] NULL,
	[long] [float] NULL,
	[demonym] [nvarchar](50) NULL,
	[area] [float] NULL,
	[gini] [float] NULL,
	[timezones] [nvarchar](50) NULL,
	[borders] [nvarchar](100) NULL,
	[native_name] [nvarchar](100) NULL,
	[numericCode] [int] NULL,
	[currencies_code] [nvarchar](50) NULL,
	[currencies_name] [nvarchar](50) NULL,
	[currencies_symbol] [nvarchar](10) NULL,
	[lang_iso639_1] [nvarchar](10) NULL,
	[lang_iso639_2] [nvarchar](10) NULL,
	[lang_name] [nvarchar](50) NULL,
	[lang_native_name] [nvarchar](50) NULL,
	[flag] [nvarchar](50) NULL,
	[cioc] [nvarchar](50) NULL,
	[url] [nvarchar](250) NULL,
 CONSTRAINT [PK_country_info] PRIMARY KEY CLUSTERED 
(
	[name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
