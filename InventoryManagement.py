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
import random

class InventoryManagement:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("InventoryManagement")

    def get_inventory(self) -> list:
        """
        :return inventory_contents: returns a list of dict corresponding to each row in the inventory table
        """
        return self.db_handler.fetch_table(Inventory)

    def order_inventory(self, item_name: str, quantity: int, category: str) -> None:
        """
        Orders more of a particular item. If the item does not exist in the database, it is added.
        
        :param item_name: the name of the item which is being ordered
        :param quantity: the amount of the item to add
        :param category: the category the item belongs to (only needed if the item is not already in the database)
        """
        if self.db_handler.contains(Inventory, {"item_name": item_name}):
            item_row = self.db_handler.fetch(Inventory, {"item_name": item_name})
            new_quantity = item_row["quantity"] + quantity
            self.db_handler.update(Inventory, {"item_name": item_name}, {"quantity": new_quantity})
        else:
            # Setting price to be random when adding a new item
            self.db_handler.insert(Inventory(item_name=item_name, category=category, price=random.randint(1, 50),quantity=quantity))
