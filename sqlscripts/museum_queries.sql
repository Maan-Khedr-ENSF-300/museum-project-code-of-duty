
-- 1) Show all tables and explain how they are related to one another (keys, triggers, etc.)
SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE table_schema = 'museum'

-- 2) A basic retrieval query 
-- Write a query to list all artist names, the year they were born, and where they are from.
SELECT AName, DateBorn, Country_origin
FROM ARTIST AS A, ART_OBJECT AS O
WHERE A.AName = O.C_AName;

-- 3) A retrieval query with ordered results
-- Write a query to list the art object ID Numbers, title, and the years they were produced. Order your list from oldest to latest.
SELECT A.ID_no AS "ID Number", A.Title AS "Title", A.Yr AS "Year"
FROM ART_OBJECT AS A
ORDER BY A.Yr ASC;

-- 4) A nested retrieval query
-- Write a query that displays the art object ID number, artist name, and year produced for all art objects that have the 
-- same origin as the artist "Leonardo Da Vinci"
SELECT O.Id_no, A.AName, O.Yr 
FROM  ART_OBJECT AS O, ARTIST AS A
WHERE O.C_AName = A.AName AND O.Origin IN(
	SELECT A.Country_origin
	FROM  ARTIST AS A
	WHERE A.AName = "Leonardo Da Vinci"  
);

-- 5) A retrieval query using joined tables
-- Write a query to list the ID number and title of the sculptures and paintings that have the style "modern"
SELECT A.Id_No, A.Title
FROM ART_OBJECT A
WHERE A.Style = "Modern" AND A.Id_No IN
	(SELECT AId_No
	 FROM ART_OBJECT A RIGHT JOIN PAINTING P ON A.Id_No = P.AId_No
		UNION ALL
		SELECT AId_No
		FROM ART_OBJECT A RIGHT JOIN SCULPTURE S ON A.Id_No = S.AId_No);

-- 6) An update operation with any necessary triggers
-- Create an update trigger for the borrowed table that:
-- will not allow someone to set a borrowed date that is earlier than the current borrowed date
DROP TRIGGER IF EXISTS DATE_BORROWED_VIOLATION;
CREATE TRIGGER DATE_BORROWED_VIOLATION
BEFORE UPDATE ON BORROWED
FOR EACH ROW
SET NEW.DATE_BORROWED = if((SELECT Date_borrowed 
							FROM BORROWED
                            WHERE AId_no = OLD.AId_no) < NEW.DATE_BORROWED, NEW.DATE_BORROWED, OLD.DATE_BORROWED);

-- UPDATE OPERATION - should not work due to trigger
UPDATE BORROWED 
SET Date_borrowed = '2020-09-30'
WHERE AId_no = 2128;

-- UPDATE OPERATION - should  work 
UPDATE BORROWED 
SET Date_borrowed = '2020-10-04'
WHERE AId_no = 2128;

-- 7) A deletion operation with any necessary triggers
-- Create a delete trigger for the PERMANENT_COLLECTION table that:
-- stores all objects removed into an archived table

DROP TRIGGER IF EXISTS ARCHIVE_COLLECTION;
CREATE TRIGGER ARCHIVE_COLLECTION
AFTER DELETE ON PERMANENT_COLLECTION FOR EACH ROW
	INSERT INTO ARCHIVED (AId_no, Stat, Cost, Date_acquired)
	VALUES(OLD.AId_no, OLD.Stat, OLD.Cost, OLD.Date_acquired);

-- DELETION OPERATION
DELETE FROM PERMANENT_COLLECTION WHERE AId_no = 1350 OR AId_no = 1448 OR AId_no = 1457;
