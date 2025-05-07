USE company_system;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- نضيف حساب أدمن تجريبي
INSERT INTO users (username, password) VALUES ('admin', 'admin123');
USE company_system;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS employees;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    national_id VARCHAR(20) NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    salary DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    passport_number VARCHAR(20),
    address VARCHAR(100),
    device_serial VARCHAR(50),
    entry_time TIME,
    exit_time TIME
);
INSERT INTO employees 
(first_name, last_name, national_id, job_title, salary, passport_number, address, device_serial, entry_time, exit_time)
VALUES
('Ahmed', 'Ali', '12345678901234', 'Nurse', 4000.00, 'A1111111', 'Doha', 'DEV001', '08:00:00', '16:00:00'),
('Sara', 'Hassan', '23456789012345', 'Technician', 5000.00, 'B2222222', 'Doha', 'DEV002', '09:00:00', '17:00:00'),
('Omar', 'Yousef', '34567890123456', 'Cleaner', 3000.00, 'C3333333', 'Doha', 'DEV003', '08:30:00', '13:30:00');
