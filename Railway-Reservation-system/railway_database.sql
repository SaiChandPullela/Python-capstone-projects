USE railway;

CREATE TABLE users (
    user_id VARCHAR(5) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    hometown VARCHAR(50) NOT NULL
    );


CREATE TABLE trains (
    train_number VARCHAR(5) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    day_of_train VARCHAR(10) NOT NULL
);


CREATE TABLE train_classes (
    train_number VARCHAR(5),
    class_name ENUM('1AC', '2AC', 'SL') NOT NULL,
    seats INT NOT NULL,
    fare DECIMAL(10 , 2 ) NOT NULL,
    PRIMARY KEY (train_number , class_name),
    FOREIGN KEY (train_number)
        REFERENCES trains (train_number)
);


CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(5) NOT NULL,
    source_station VARCHAR(255) NOT NULL,
    destination_station VARCHAR(255) NOT NULL,
    day_of_travel DATE NOT NULL,
    ticket_class VARCHAR(10) NOT NULL,
    train_number VARCHAR(10) NOT NULL,
    pnr_number VARCHAR(6) NOT NULL UNIQUE,
    fare DECIMAL(10 , 2 ) NOT NULL,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id),
    FOREIGN KEY (train_number)
        REFERENCES trains (train_number)
);


INSERT INTO trains (train_number, name, arrival_time, departure_time, day_of_train)
VALUES
('12345', 'Odisha Express', '12:34', '22:12', 'Wednesday'),
('12346', 'Rajdhani Express', '05:30', '22:00', 'Monday'),
('12627', 'Karnataka Express', '08:20', '20:30', 'Sunday'),
('12951', 'Mumbai Rajdhani', '08:35', '16:40', 'Thursday'),
('12138', 'Punjab Mail', '04:30', '23:45', 'Saturday'),
('12295', 'Sanghamitra Express', '12:50', '21:45', 'Wednesday'),
('12029', 'New Delhi Shatabdi', '11:05', '15:45', 'Monday'),
('12841', 'Coromandel Express', '19:20', '22:50', 'Friday'),
('12618', 'Mangala Lakshadweep Express', '12:30', '17:45', 'Tuesday'),
('12278', 'Duronto Express', '06:25', '14:55', 'Sunday'),
('12723', 'Telangana Express', '14:40', '20:30', 'Thursday'),
('12565', 'Bihar Sampark Kranti', '05:10', '19:50', 'Wednesday');


INSERT INTO train_classes (train_number, class_name, seats, fare)
VALUES
-- Example 1: Odisha Express
('12345', '1AC', 30, 2205),
('12345', '2AC', 23, 1190),
('12345', 'SL', 43, 234),
-- Example 2: Rajdhani Express
('12346', '1AC', 40, 3450),
('12346', '2AC', 35, 1950),
('12346', 'SL', 50, 500),
-- Example 3: Karnataka Express
('12627', '1AC', 25, 2450),
('12627', '2AC', 35, 1350),
('12627', 'SL', 60, 400),
-- Example 4: Mumbai Rajdhani
('12951', '1AC', 30, 2950),
('12951', '2AC', 40, 1750),
('12951', 'SL', 70, 600),
-- Example 5: Punjab Mail
('12138', '1AC', 20, 2200),
('12138', '2AC', 30, 1200),
('12138', 'SL', 55, 350),
-- Example 6: Sanghamitra Express
('12295', '1AC', 28, 2700),
('12295', '2AC', 38, 1500),
('12295', 'SL', 65, 450),
-- Example 7: New Delhi Shatabdi
('12029', '1AC', 20, 3100),
('12029', '2AC', 35, 1650),
('12029', 'SL', 50, 550),
-- Example 8: Coromandel Express
('12841', '1AC', 30, 2850),
('12841', '2AC', 45, 1550),
('12841', 'SL', 75, 500),
-- Example 9: Mangala Lakshadweep Express
('12618', '1AC', 28, 2600),
('12618', '2AC', 42, 1450),
('12618', 'SL', 68, 420),
-- Example 10: Duronto Express
('12278', '1AC', 32, 3050),
('12278', '2AC', 50, 1800),
('12278', 'SL', 80, 600),
-- Example 11: Telangana Express
('12723', '1AC', 24, 2500),
('12723', '2AC', 36, 1400),
('12723', 'SL', 64, 420),
-- Example 12: Bihar Sampark Kranti
('12565', '1AC', 22, 2300),
('12565', '2AC', 38, 1300),
('12565', 'SL', 70, 380);







