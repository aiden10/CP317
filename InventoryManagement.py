"""
Uses: 
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

"""

from DatabaseHandler import DatabaseHandler
from Logger import Logger

class InventoryManagement:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("InventoryManagement")

    def get_inventory(self) -> list:
        return self.db_handler.fetch_table("inventory")

    def order_inventory(self, item_name: str, quantity: int) -> None:
        if len(self.db_handler.fetch((item_name), "inventory", "item_name")) > 0:            
            # Needing to access specific column values by index isn't really great and requires referencing the tables.sql file
            prev_quantity = self.db_handler.fetch((item_name), "inventory", "item_name")[0][3] # Access the first row's third column (quantity)
            self.db_handler.update((prev_quantity + quantity), item_name, "inventory", "quantity", "item_name")
            return
        
        self.db_handler.insert((item_name, quantity), "inventory")

