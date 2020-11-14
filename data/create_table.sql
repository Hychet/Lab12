
PRAGMA foreign_keys = OFF;
DROP TABLE users;
DROP TABLE Posts;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, hash INTEGER);
CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY ASC, poster CONSTRAINT cons REFERENCES users(username), title TEXT, content TEXT, );

SELECT * FROM users;