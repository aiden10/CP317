
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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy        

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db = SQLAlchemy()
db.init_app(app)

# Class to handle database operations
class DatabaseHandler:
    def __init__(self):
        self.logger = Logger("DatabaseHandler")

    def create_tables(self) -> None:
        with app.app_context():
            db.create_all()

    def drop_all(self) -> None:
        """
        Clears the database
        """
        db.drop_all()

    def contains(self, table, condition) -> bool:
        """
        Checks if at least one record matches the given condition  

        Usage: result = db_handler.contains(ModelName, {"column1": value1, "column2": value2})  
        
        :param table: the model class representing the table to search in  
        :param condition: a dictionary containing the attributes and their values to check for existence  

        :return bool: indicating whether at least one matching record exists  
        """
        try:
            with app.app_context():
                exists = db.session.query(table).filter_by(**condition).first() is not None
                return exists
        except Exception as e:
            self.logger.write_log(f"Contains check failed: {e}")
            return False


    def insert(self, record) -> bool:
        """
        Inserts a row into a table

        Usage: result = db_handler.insert(model(attr1 = data1, attr2 = data2, attr3 = data3, ...))
        
        :param record: the object containing the data to be inserted
        
        :return bool: indicating whether the insertion was successful or not
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

    def delete(self, table, condition) -> bool:
        """
        Deletes any row(s) from a table matching the condition
        
        Usage: result = db_handler.delete(model, {attr:value})
        
        :param table: the model/table where the data will be deleted
        :param condition: the dict containing the data which will be checked 

        :return bool: indicating whether the deletion was successful or not
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

    def update(self, table, condition, updates) -> bool:
        """ 
        Updates first record matching the condition with new values
        
        Usage: result = db_handler.update(model, {condition_attr: val}, {update_attr: val})
        
        :param table: the model/table which will be searched
        :param condition: the dict containing the data which will be checked
        :param updates: the dict containing the new column, data pair
        
        :return bool: indicating whether the table was updated or not
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

    def fetch(self, table, condition) -> dict:
        """
        Returns the rows matching the condition

        Usage: result = db_handler.fetch(model, {attr:value})

        :param table: the model/table which will be searched
        :param condition: the tuple containing the data which will be checked

        :return matches: any object matching condition
        """
        try:
            with app.app_context():
                matches = db.session.query(table).filter_by(**condition).all() # double asterisks for unpacking dictionary
                self.logger.write_log("Row fetched successfully.")
                return self._retrieve_data(matches)
        except Exception as e:
            self.logger.write_log(f"Row fetch failed: {e}")
            return None

    def fetch_table(self, table) -> list[dict]:
        """
        Returns a list of all objects from the table

        Usage: results = db_handler.fetch_table(model)

        :param table: the model/table to retrieve data from
        :return results: list of all the objects/rows in the table
        """
        try:
            with app.app_context():
                self.logger.write_log("Table fetched successfully.")
                return self._retrieve_data(db.session.query(table).all())
            
        except Exception as e:
            self.logger.write_log(f"Table fetch failed: {e}")
            return None

    def _retrieve_data(self, matches):
        """
        Private function to convert retrieved matches to a more convenient format

        :param matches: list of Table objects

        :return values: list of dict or single dict containing table properties and values.
        """

        values = []
        if matches:
            for match in matches:
                entry = {}
                properties = match.__dict__.keys()
                for property in properties:
                    if property == '_sa_instance_state':
                        continue
                    entry.update({property: match.__dict__[property]})
                
                values.append(entry)
        
        if len(values) == 1:
            return values[0]
        
        return values