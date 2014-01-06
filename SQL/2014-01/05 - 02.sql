/*
	add Title to Projects and Tasks
*/


ALTER TABLE Projects
ADD Title varchar(100) NOT NULL DEFAULT ''

ALTER TABLE Tasks
ADD Title varchar(100) NOT NULL DEFAULT ''