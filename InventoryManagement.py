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
        self.logger = Logger()

    def get_inventory(self) -> list:
        self.db_handler.fetch_table("inventory")

    def order_inventory(self, item_name: str, quantity: int) -> None:
        if self.db_handler.contains(item_name, "inventory"):
            
            # These two lines wouldn't really work which is why the update function needs to be modified once we know what database we're using
            prev_quantity = self.db_handler.fetch_row(item_name, "inventory")
            self.db_handler.update(item_name, prev_quantity + quantity, "inventory")
            
            return
        
        self.db_handler.insert((item_name, quantity), "inventory")

