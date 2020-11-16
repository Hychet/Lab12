
PRAGMA foreign_keys = OFF;
DROP TABLE users;
DROP TABLE posts;
DROP TABLE votes;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, hash INTEGER);
CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, poster CONSTRAINT cons REFERENCES users(username), title TEXT, content TEXT, score INTEGER, dateposted TEXT);
CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY ASC, postid CONSTRAINT cons REFERENCES posts(id), username CONSTRAINT cons REFERENCES users(username), vote INTEGER);

SELECT * FROM users;