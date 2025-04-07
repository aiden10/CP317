"""
Uses: 
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

"""

from DatabaseHandler import DatabaseHandler
from Logger import Logger
from Tables import Inventory

class InventoryManagement:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("InventoryManagement")

    def get_inventory(self) -> list:
        return self.db_handler.fetch_table(Inventory)

    def order_inventory(self, item_name: str, quantity: int) -> None:
        ...