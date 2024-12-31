CREATE DATABASE Space;

USE Space;

CREATE TABLE SpaceCraft (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('Rocket', 'Shuttle') NOT NULL,
    capacity INT NOT NULL,
    current_fuel INT NOT NULL
);

CREATE TABLE Astronaut (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    `rank` VARCHAR(255) NOT NULL,
    experience_years INT NOT NULL,
    weight INT NOT NULL
);

CREATE TABLE Mission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mission_name VARCHAR(255) NOT NULL,
    spacecraft_id INT,
    status ENUM('Launched', 'Pending') NOT NULL,
    FOREIGN KEY (spacecraft_id) REFERENCES SpaceCraft(id)
);