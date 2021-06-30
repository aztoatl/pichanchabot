#QSL statements to create a new empty database
CREATE TABLE `badans` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`answer`	TEXT
)
CREATE TABLE "respuestas" (
	`AnswId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`AnswCreator`	TEXT,
	`Answfield`	TEXT NOT NULL
)
CREATE TABLE sqlite_sequence(name,seq)
