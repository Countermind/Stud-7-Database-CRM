/*
	remove EntityID from Authorizations
*/

BEGIN TRAN

	ALTER TABLE Authorizations
	DROP CONSTRAINT FK__Authoriza__Entit__0519C6AF
	GO

	DELETE FROM Entities
	WHERE EXISTS(
		SELECT *
		FROM Authorizations
		WHERE Authorizations.EntityID = Entities.EntityID
		)

	ALTER TABLE Authorizations
	DROP COLUMN EntityID

COMMIT