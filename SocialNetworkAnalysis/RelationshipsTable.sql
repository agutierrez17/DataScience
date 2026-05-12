USE [Philanthropy]
GO

/****** Object:  Table [dbo].[Transactions]    Script Date: 4/1/2026 8:47:55 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Relationships](
	[Unique Key] [numeric](10,0) NOT NULL,
	[Recip Key] [numeric](10,0) NOT NULL,
	[ID] [varchar](50) NULL,
	[Related ID] [varchar](50) NULL,
	[Relationship Type] [varchar](100) NULL,
	[Status] [varchar](50) NULL
) ON [PRIMARY]
GO


