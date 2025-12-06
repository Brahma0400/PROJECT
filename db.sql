drop database if exists phishing;
create database phishing;
use phishing;

create table users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(225),
    email VARCHAR(50), 
    password VARCHAR(50),
    attempts INT DEFAULT 3
    );

create table reviews (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    email VARCHAR(225),
    rating INT,
    feedback VARCHAR(1000)
    );