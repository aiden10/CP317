
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
from Server import app, db

# Class to handle database operations
class DatabaseHandler:
    def __init__(self):
        self.logger = Logger("DatabaseHandler")

    def contains(self, table, condition):
        """
        Parameters:  
            - table: the model class representing the table to search in  
            - condition: a dictionary containing the attributes and their values to check for existence  

        Returns:  
            - a bool indicating whether at least one matching record exists  

        Usage:  
            result = db_handler.contains(ModelName, {"column1": value1, "column2": value2})  

        Checks if at least one record matches the given condition  
        """
        try:
            with app.app_context():
                exists = db.session.query(table).filter_by(**condition).first() is not None
                return exists
        except Exception as e:
            self.logger.write_log(f"Contains check failed: {e}")
            return False


    def insert(self, record):
        """
        Parameters: 
            - record: the object containing the data to be inserted
        Returns:
            - a bool indicating whether the insertion was successful or not

        Usage:
            result = db_handler.insert(model(attr1 = data1, attr2 = data2, attr3 = data3, ...))
            
        Inserts a row into a table
        """
        try:
            with app.app_context():
                db.session.add(record)
                db.session.commit()
                self.logger.write_log(f"Inserted new record into {record.__tablename__}.")
                return True
        except Exception as e:
            self.logger.write_log(f"Insert failed: {e}")
            return False

    def delete(self, table, condition):
        """
        Parameters: 
            - table: the model/table where the data will be deleted
            - condition: the dict containing the data which will be checked 
        Returns:
            - a bool indicating whether the deletion was successful or not

        Usage:
            result = db_handler.delete(model, {attr:value})
        Deletes any row(s) from a table matching the condition
        """
        deleted = False
        try:
            with app.app_context():
                deleted = db.session.query(table).filter_by(**condition).delete(synchronize_session=False)
                db.session.commit()
                if deleted > 0:
                    self.logger.write_log("Row deleted successfully.")
                    deleted = True
                else:
                    self.logger.write_log("No matching row to delete.")
        except Exception as e:
            self.logger.write_log(f"Delete failed: {e}")
        return deleted

    def update(self, table, condition, updates):
        """
        Parameters: 
            - table: the model/table which will be searched
            - condition: the dict containing the data which will be checked
            - updates: the dict containing the new column, data pair
        Returns:
            - a bool indicating whether the table was updated or not

        Usage:
            result = db_handler.update(model, {condition_attr: val}, {update_attr: val})
            
       Updates first record matching the condition with new values
       """
        try:
            with app.app_context():
                record = db.session.query(table).filter_by(**condition).first()
                if record:
                    for key, value in updates.items():
                        setattr(record, key, value)
                    db.session.commit()
                    self.logger.write_log("Row updated successfully.")
                    return True
                self.logger.write_log("No matching row to update.")
                return False
        except Exception as e:
            self.logger.write_log(f"Update failed: {e}")
            return False

    def fetch(self, table, condition):
        """
        Parameters:  
            - table: the model/table which will be searched
            - condition: the tuple containing the data which will be checked
        Returns:
            - matches: any object matching condition

        Usage:
            result = db_handler.fetch(model, {attr:value})
        Returns all records matching the condition
        """
        try:
            with app.app_context():
                matches = db.session.query(table).filter_by(**condition).all() # double asterisks for unpacking dictionary
                self.logger.write_log("Row fetched successfully.")
                return matches
        except Exception as e:
            self.logger.write_log(f"Row fetch failed: {e}")
            return None

    def fetch_table(self, table):
        """
        Parameters: 
            - table: the model/table to retrieve data from
        Returns:
            - a list of all the objects/rows in the table

        Usage:
            results = db_handler.fetch_table(model)

        Returns a list of all objects from the table
        """
        try:
            with app.app_context():
                self.logger.write_log("Table fetched successfully.")
                return db.session.query(table).all()
        except Exception as e:
            self.logger.write_log(f"Table fetch failed: {e}")
            return None
#old code
#---------------------------
# import mysql.connector

# class DatabaseHandler:
#     def __init__(self):
#         self.database = mysql.connector.connect(
#             host = "localhost", # [CHANGE] Change this string to host of the database we are using 
#             user = "username", # [CHANGE] Change this string to username database is using
#             password = "password", # [CHANGE] Change this string to password database is using
#             database = "database" # [CHANGE] Change this string to the name of the database we are using
#         )
#         self.logger = Logger("DatabaseHandler")
#         self.cursor = self.database.cursor()
        
#     def insert(self, data: tuple, table: str, column_names: list[str]) -> bool:
#         """
#         Parameters: 
#             - data: the tuple containing the data to be inserted
#             - table: the name of the table where the data will be inserted
#             - column_names: the names of the columns where the data will be inserted
#         Returns:
#             - a bool indicating whether the insertion was successful or not

#         Usage:
#             result = db_handler.insert((data1, data2, data3), "sample_table", ["column1", "column2", "column3"])
#             if result:
#                 ...
#         Inserts a row into a table
#         """
#         assert len(column_names) == len(data), "data must contain the same amount of elements as column names"

#         # Insert rows into database
#         sql_statement = f"INSERT INTO {table} ({', '.join(column_names)}) VALUES {', '.join(['%s'] * len(column_names))}"
#         self.cursor.execute(sql_statement, data)
#         self.database.commit(); # Commit / apply changes to database
        
#         # Return False if no rows were changed
#         if self.cursor.rowcount <= 0:
#             self.logger.write_log(f"Failed to insert: {data} into table: {table}")
#             return False
        
#         return True
    
#     # Deletes specified data from the database
#     def delete(self, condition: tuple, table: str, column_name: str) -> bool:
#         """
#         Parameters: 
#             - condition: the tuple containing the data which will be checked 
#             - table: the name of the table where the data will be deleted
#             - column_name: the name of the column potentially containing the condition
#         Returns:
#             - a bool indicating whether the deletion was successful or not

#         Usage:
#             result = db_handler.delete((condition1), "sample_table", "condition1")
#             if result:
#                 ...
#         Deletes row(s) from a table
#         """

#         sql_statement = f"DELETE FROM {table} WHERE {column_name} = %s"

#         self.cursor.execute(sql_statement, condition)
#         self.database.commit() # Commit / apply changes to database
        
#         # Return False if no rows were changed
#         if self.cursor.rowcount <= 0:
#             self.logger.write_log(f"Failed to delete rows matching {condition} into table: {table}")
#             return False
        
#         return True

#     def fetch(self, condition: tuple, table: str, column_name: str) -> list[tuple]:
#         """
#         Parameters: 
#             - condition: the tuple containing the data which will be checked 
#             - table: the name of the table which will be searched
#             - column_name: the name of the column potentially containing the condition
#         Returns:
#             - the row(s) containing the data

#         Usage:
#             result = db_handler.fetch((condition1), "sample_table", "condition1")
#             if result:
#                 ...
#         Returns all records matching the condition
#         """

#         sql_statement = f"SELECT * FROM {table} WHERE {column_name} = %s"
#         self.cursor.execute(sql_statement, condition)
#         results = self.cursor.fetchall() # Retrieves results of most recent query that has been executed (empty if no result)
        
#         if len(results) <= 0:
#             self.logger.write_log(f"Found no rows matching condition: {column_name} = {condition}")
#             return []
        
#         return results
    
#     def update(self, new_data: tuple, condition: tuple, table: str, set_column: str, where_column: str) -> bool: 
#         """
#         Parameters: 
#             - new_data: the variable containing the new data
#             - condition: the variable containing the data which will be checked 
#             - table: the name of the table which will be searched
#             - set_column: the name of the column whose values will be modified
#             - where_column: the name of the column which is checked for matching the condition
#         Returns:
#             - a bool indicating whether the table was updated or not

#         Usage:
#             result = db_handler.update((new_quantity), item_name, "inventory", "quantity", "item_name") 
#             Read as: UPDATE inventory SET quantity = new_quantity WHERE item_name = item_name
            
#         Updates column values to new_data where the existing column value matches condition
#         """
#         sql_statement = f"UPDATE {table} SET {set_column} = %s WHERE {where_column} = %s"
#         self.cursor.execute(sql_statement, (new_data, condition))
#         self.database.commit()
#         if self.cursor.rowcount <= 0:
#             self.logger.write_log(f"Failed to update: {set_column} to {new_data} WHERE {where_column} = {condition}")
#             return False
        
#         return True

#     def fetch_table(self, table: str) -> list[tuple]:
#         """
#         Parameters: 
#             - table: the name of the table to retrieve data from
#         Returns:
#             - a list of all the rows in the table

#         Usage:
#             results = db_handler.fetch_table("table_name")

#         Retrieves all rows from a table
#         """
#         sql_statement = f"SELECT * FROM {table}"
#         self.cursor.execute(sql_statement)
#         return self.cursor.fetchall()
