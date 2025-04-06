# About
(Created for CP317, Software Engineering)

The Grocery Store Finance Tracker (GSFT) is a software designed for grocery store owners and employees to manage their finances, sales, employees, and inventory in a convenient, secure way. It also allows customers to track their spending and finances.

# Features
- Owners
  - View sales and revenue information
  - Manage Employees
  - Manage Inventory

- Employees
  - Manage Inventory

- Customers
  - View spending information

# Hosting
Currently, the GSFT is not hosted online and must be run locally. 

To get started, first cd into the CP317 directory and run `pip install -r requirements.txt`to get the required Python dependencies.

Next, host the server on your local netword by running the Server.py file.

Lastly, run: `python -m http.server 8000` to host the front end. 

# Usage
Once the GSFT application is running locally on your device, navigate to `localhost:8000/register` to create a new account. You will automatically be redirected to the dashboard.
