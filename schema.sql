
CREATE DATABASE IF NOT EXISTS chat;
use chat;


CREATE TABLE Users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    age INT NOT NULL CHECK (age > 17),
    gender ENUM('male', 'female'),
    country VARCHAR(255),
    region VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)


CREATE TABLE tokenUsage(
    username VARCHAR(255),
    refresh_token CHAR(64) NOT NULL UNIQUE, 
    expires_at DATETIME NOT NULL,
    FOREIGN KEY(username) REFERENCES Users(username)
)
