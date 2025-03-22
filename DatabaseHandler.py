
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
"""

from Logger import Logger

class DatabaseHandler:
    def __init__(self):
        self.logger = Logger()
    
    def insert(data, table: str) -> bool:
        ...
    def delete(data, table: str) -> bool:
        ...
    def contains(data, table: str) -> bool:
        ...
    
    """
    These functions are a bit more complex because sometimes you might want to conditionally update or fetch something.
    Could be modified to use an SQL query if we use an SQL database.
    """
    def update(data, new_data, table: str) -> bool: 
        """
        Replaces instances of data with new_data
        """
        ...
    def fetch_row(condition, table: str) -> list:
        ...
        
    def fetch_table(table: str) -> list:
        ...