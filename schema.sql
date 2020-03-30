DROP DATABASE timbot;
CREATE DATABASE timbot;
USE timbot;

CREATE TABLE users (
	uid integer PRIMARY KEY AUTO_INCREMENT,
	name varchar(191) UNIQUE NOT NULL
);

CREATE TABLE webopoly (
	uid integer NOT NULL,
	wins integer NOT NULL,
	FOREIGN KEY (uid) REFERENCES users(uid)
);
