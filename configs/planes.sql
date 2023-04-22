

CREATE TABLE IF NOT EXISTS Logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modul VARCHAR(255) NOT NULL,
    text VARCHAR(255) NOT NULL,
    lvl  VARCHAR(255) NOT NULL, 
    info VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) 
CREATE TABLE IF NOT EXISTS flight (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start VARCHAR(40),
    start_short VARCHAR(9),
    destination VARCHAR(40),
    destination_short VARCHAR(9),
    stops int(10),
    stops_dest VARCHAR(255),
    airline VARCHAR(255),
    add_infos  VARCHAR(255),
    Start_Date DATE,
    End_Date DATE,
    duration  VARCHAR(40), 
    price int(40), 
    currancy VARCHAR(40),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) 

CREATE TABLE IF NOT EXISTS airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    int_short VARCHAR(10) UNIQUE,
    city VARCHAR(40),
    land VARCHAR(40),
    continent VARCHAR(100),
    coord_N VARCHAR(255),
    coord_O VARCHAR(255),
    search_A TINYINT(1),
    search_B TINYINT(1),
    search_C TINYINT(1),
    regex3 VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_changed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) 



CREATE TABLE IF NOT EXISTS airports (
    name VARCHAR(255),
    city VARCHAR(40),
    land VARCHAR(40),
    continent VARCHAR(100),
    coord_N VARCHAR(255),
    coord_O VARCHAR(255),
    search_B TINYINT(1),
    regex3 VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_changed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) 