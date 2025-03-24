
"""
Uses: 
    - Logger

Called From:
    - AuthenticationHandler
    - InventoryManagement
    - FinanceModule
    - ReportGenerator
    - EmployeeManagement
    - AssetManagement

The delete, fetch, and update functions may need to be updated to support greater than or less than conditions
"""

from Logger import Logger

import mysql.connector


class DatabaseHandler:
    def __init__(self):
        self.database = mysql.connector.connect(
            host = "localhost", # [CHANGE] Change this string to host of the database we are using 
            user = "username", # [CHANGE] Change this string to username database is using
            password = "password", # [CHANGE] Change this string to password database is using
            database = "database" # [CHANGE] Change this string to the name of the database we are using
        )
        self.logger = Logger("DatabaseHandler")
        self.cursor = self.database.cursor()
        
    def insert(self, data: tuple, table: str, column_names: list[str]) -> bool:
        """
        Parameters: 
            - data: the tuple containing the data to be inserted
            - table: the name of the table where the data will be inserted
            - column_names: the names of the columns where the data will be inserted
        Returns:
            - a bool indicating whether the insertion was successful or not

        Usage:
            result = db_handler.insert((data1, data2, data3), "sample_table", ["column1", "column2", "column3"])
            if result:
                ...
        Inserts a row into a table
        """
        assert len(column_names) == len(data), "data must contain the same amount of elements as column names"

        # Insert rows into database
        sql_statement = f"INSERT INTO {table} ({', '.join(column_names)}) VALUES {', '.join(['%s'] * len(column_names))}"
        self.cursor.execute(sql_statement, data)
        self.database.commit(); # Commit / apply changes to database
        
        # Return False if no rows were changed
        if self.cursor.rowcount <= 0:
            self.logger.write_log(f"Failed to insert: {data} into table: {table}")
            return False
        
        return True
    
    # Deletes specified data from the database
    def delete(self, condition: tuple, table: str, column_name: str) -> bool:
        """
        Parameters: 
            - condition: the tuple containing the data which will be checked 
            - table: the name of the table where the data will be deleted
            - column_name: the name of the column potentially containing the condition
        Returns:
            - a bool indicating whether the deletion was successful or not

        Usage:
            result = db_handler.delete((condition1), "sample_table", "condition1")
            if result:
                ...
        Deletes row(s) from a table
        """

        sql_statement = f"DELETE FROM {table} WHERE {column_name} = %s"

        self.cursor.execute(sql_statement, condition)
        self.database.commit() # Commit / apply changes to database
        
        # Return False if no rows were changed
        if self.cursor.rowcount <= 0:
            self.logger.write_log(f"Failed to delete rows matching {condition} into table: {table}")
            return False
        
        return True

    def fetch(self, condition: tuple, table: str, column_name: str) -> list[tuple]:
        """
        Parameters: 
            - condition: the tuple containing the data which will be checked 
            - table: the name of the table which will be searched
            - column_name: the name of the column potentially containing the condition
        Returns:
            - the row(s) containing the data

        Usage:
            result = db_handler.fetch((condition1), "sample_table", "condition1")
            if result:
                ...
        Returns all records matching the condition
        """

        sql_statement = f"SELECT * FROM {table} WHERE {column_name} = %s"
        self.cursor.execute(sql_statement, condition)
        results = self.cursor.fetchall() # Retrieves results of most recent query that has been executed (empty if no result)
        
        if len(results) <= 0:
            self.logger.write_log(f"Found no rows matching condition: {column_name} = {condition}")
            return []
        
        return results
    
    def update(self, new_data, condition, table: str, column_name: str) -> bool: 
        """
        Parameters: 
            - new_data: the variable containing the new data
            - condition: the variable containing the data which will be checked 
            - table: the name of the table which will be searched
            - column_name: the name of the column potentially containing the condition
        Returns:
            - a bool indicating whether the table was updated or not

        Usage:
            result = db_handler.update(100, 50, "table_name", "count")
            if result:
                ...
        Updates column values to new_data where the existing column value matches condition
        """
        sql_statement = f"UPDATE {table} SET {column_name} = %s WHERE {column_name} = %s"
        self.cursor.execute(sql_statement, (new_data, condition))
        self.database.commit()
        if self.cursor.rowcount <= 0:
            self.logger.write_log(f"Failed to update: {column_name} to {new_data} WHERE {column_name} = {condition}")
            return False
        
        return True

    def fetch_table(self, table: str) -> list[tuple]:
        """
        Parameters: 
            - table: the name of the table to retrieve data from
        Returns:
            - a list of all the rows in the table

        Usage:
            results = db_handler.fetch_table("table_name")

        Retrieves all rows from a table
        """
        sql_statement = f"SELECT * FROM {table}"
        self.cursor.execute(sql_statement)
        return self.cursor.fetchall()
