CREATE DATABASE CRM
GO
USE CRM
GO

CREATE TABLE Entities(
EntityID bigint NOT NULL IDENTITY(1,1) PRIMARY KEY,
Created date NOT NULL,
CreatedByUserID int NULL,
Updated date NULL,
UpdatedByUserID int NULL,
Deleted date NULL,
ObjectID bigint NOT NULL
)
GO

CREATE TABLE Authorizations(
[Login] varchar(20) NOT NULL PRIMARY KEY,
EntityID bigint NOT NULL REFERENCES Entities(EntityID),
[Password] varchar(50) NOT NULL
)

CREATE TABLE Users(
UserID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
EntityID bigint NOT NULL REFERENCES Entities(EntityID),
FirstName varchar(20) NOT NULL,
LastName varchar(20) NOT NULL,
LoginID varchar(20) NOT NULL REFERENCES Authorizations([Login])
)
GO

ALTER TABLE Entities
ADD CONSTRAINT FK_CreatedByUserID_Users FOREIGN KEY (CreatedByUserID)
	REFERENCES Users(UserID),
CONSTRAINT FK_UpdatedByUserID_Users FOREIGN KEY (UpdatedByUserID)
	REFERENCES Users(UserID)
GO

CREATE TABLE ContactInfoTypes(
ContactInfoTypeID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
ContactInfoTypeName varchar(10)
)

CREATE TABLE ContactInfo(
Contact varchar(40) NOT NULL,
UserID int NOT NULL REFERENCES Users(UserID),
ContactInfoTypeID int NOT NULL REFERENCES ContactInfoTypes(ContactInfoTypeID)
)

CREATE TABLE Clients(
ClientID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
UserID int NOT NULL REFERENCES Users(UserID)
)
GO

CREATE TABLE Employees(
EmployeeID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
UserID int NOT NULL REFERENCES Users(UserID),
TimeZone int NOT NULL,
BirthDate date NULL,
)
GO

CREATE TABLE ProjectStatuses(
ProjectStatusID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
StatusName varchar(20) NOT NULL
)
GO

CREATE TABLE Projects(
ProjectID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
EntityID bigint NOT NULL REFERENCES Entities(EntityID),
ClientID int REFERENCES Clients(ClientID),
ProjectStart date,
MonthPaymentDollars decimal(19,2),
ProjectStatusID int NOT NULL REFERENCES ProjectStatuses(ProjectStatusID)
)
GO

CREATE TABLE TaskStatuses(
TaskStatusID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
StatusName varchar(20) NOT NULL
)
GO

CREATE TABLE Tasks(
TaskID int NOT NULL IDENTITY(1,1) PRIMARY KEY,
EntityID bigint NOT NULL REFERENCES Entities(EntityID),
ProjectID int NOT NULL REFERENCES Projects(ProjectID),
TaskStatusID int NOT NULL REFERENCES TaskStatuses(TaskStatusID)
)
GO

CREATE TABLE TaskPushes(
PushDate datetime NOT NULL,
PushByEmployeeID int NOT NULL REFERENCES Employees(EmployeeID),
PushToEmployeeID int NOT NULL REFERENCES Employees(EmployeeID),
TaskID int NOT NULL REFERENCES Tasks(TaskID),
PushComment varchar(2000)
)

CREATE TABLE Jobs(
JobID bigint NOT NULL IDENTITY(1,1) PRIMARY KEY,
EntityID bigint NOT NULL REFERENCES Entities(EntityID),
TaskID int NOT NULL REFERENCES Tasks(TaskID),
[Description] varchar(200),
DurationMinutes int NOT NULL,
)