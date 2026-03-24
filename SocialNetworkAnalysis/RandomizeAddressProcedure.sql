
USE [Philanthropy]
GO

/****** Object:  StoredProcedure [dbo].[Event_Attendance_Seed]    Script Date: 3/23/2026 11:59:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[Randomize_Address] AS

DECLARE @CBSA INT
DECLARE @AddressCount INT
DECLARE @Counter INT
DECLARE @ID VARCHAR(250)
DECLARE @AddressLine1 VARCHAR (250)
DECLARE @ST VARCHAR(50)
DECLARE @ZIP VARCHAR(50)
DECLARE @City VARCHAR(50)

SET @AddressCount = (SELECT COUNT(*) FROM DBO.Addresses)
SET @Counter = 1

WHILE (@Counter <= @AddressCount)
BEGIN
	BEGIN TRANSACTION
		PRINT 'Starting insert loop'
		PRINT @Counter

		-- SELECT RANDOM ADDRESS 
		SELECT
		@ID = A3.[ID],
		@AddressLine1 = A.[Address Line 1],
		@ST = CASE WHEN A.ST IN ('PW','GU','VI','AS','MH','FM','MP','DC') THEN 'FL' ELSE A.ST END
		FROM [Philanthropy].[dbo].[Addresses] A WITH (NOLOCK)
		LEFT OUTER JOIN dbo.Addresses_3 A3 WITH (NOLOCK) ON A.[ID] = A3.ID
		WHERE
		A3.ID IS NULL
		ORDER BY 
		NEWID() OFFSET 1 ROWS

		-- SELECT CBSA BASED ON STATE
		SELECT 
		@CBSA = [CBSA code] 
		FROM geo.MetroArea_To_State S WITH (NOLOCK) 
		WHERE 
		S.[Primary State] = @ST 
		ORDER BY 
		NEWID() OFFSET 1 ROWS

		-- SELECT ZIP CODE BASED ON CBSA
		SELECT 
		@ZIP = [ZIP Code],
		@City = [USPS Default City for ZIP]
		FROM geo.[ZIP_To_TownMetroState] Z WITH (NOLOCK) 
		WHERE 
		Z.[USPS Default State for ZIP] = @ST 
		AND
		Z.[CBSA Code] = @CBSA
		ORDER BY NEWID() OFFSET 1 ROWS

		--PRINT @ID
		--PRINT @AddressLine1
		--PRINT @City
		--PRINT @ST
		--PRINT @ZIP
		--PRINT @CBSA

		-- INSERT INTO TABLE
		PRINT 'Inserting...'
		INSERT INTO DBO.Addresses_3 ([ID], [Address Line 1], [City], [ST], [ZIP]) VALUES (@ID, @AddressLine1, @City, @ST, @ZIP)

		SET @Counter = @Counter + 1
		COMMIT TRANSACTION
		PRINT 'Row inserted successfully'
END

GO