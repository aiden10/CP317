

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
    pay decmial(19, 4),
    weekly_hours float,
    primary key (employee_id)
);

-- Sales table
CREATE TABLE sales (
    owner_email varchar(255),
    amount decimal(19, 4),
    sale_date date
);

-- Revenue table
CREATE TABLE revenue (
    -- Not sure what the difference between sales and revenue is in this case
    owner_email varchar(255),
    amount decimal(19, 4)
);

-- Assets table
CREATE TABLE assets (
    -- Not sure what assets is here
    owner_email varchar(255),
);
