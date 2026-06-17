CREATE DATABASE IF NOT EXISTS  customerchurn;
use customerchurn;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    company VARCHAR(255),
    mobile VARCHAR(15) UNIQUE,
    owner_name VARCHAR(255),
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM users;


