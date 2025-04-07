

-- Sessions table
CREATE TABLE sessions (
    session_token varchar(512)
);

-- Accounts table
CREATE TABLE accounts (
    email varchar(255),
    password_hash varchar(255),
    privilege varchar(12)
);

-- Inventory table
CREATE TABLE Inventory (
    item_name varchar(255),
    category varchar(255),
    price decimal(19, 4),
    quantity int,
    primary key (item_name)
);

-- Employees table
CREATE TABLE employees (
    employee_id int,
    first_name varchar(255),
    last_name varchar(255),
    position varchar(255),
    pay decimal(19, 4),
    weekly_hours float,
    primary key (employee_id)
);

-- Sales table
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_email VARCHAR(255),
    amount DECIMAL(19, 4),
    sale_date DATE,
    FOREIGN KEY (owner_email) REFERENCES accounts(email)
);

-- Revenue table
CREATE TABLE revenue (
    revenue_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_email VARCHAR(255),
    amount DECIMAL(19, 4),
    FOREIGN KEY (owner_email) REFERENCES accounts(email)
);

-- Assets table
CREATE TABLE assets (
    asset_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_email VARCHAR(255),
    description VARCHAR(255),
    value DECIMAL(19, 4),
    FOREIGN KEY (owner_email) REFERENCES accounts(email)
);
