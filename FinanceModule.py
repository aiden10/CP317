
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - DashboardSummarizer
"""

from DatabaseHandler import DatabaseHandler
from Logger import Logger
from Tables import Sales, Revenue

class FinanceModule:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("FinanceModule")
        
    def get_sales(self, email: str) -> list:
        return self.db_handler.fetch(Sales, {"user": email})
    
    def get_revenue(self, email: str) -> list:
        return self.db_handler.fetch(Revenue, {"user": email})
