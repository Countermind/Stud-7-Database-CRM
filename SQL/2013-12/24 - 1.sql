/*
	make Entity.ObjectID column nullable
*/
USE CRM
ALTER TABLE Entities
ALTER COLUMN ObjectID bigint NULL