
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - DashboardSummarizer
"""

from DatabaseHandler import DatabaseHandler
from Logger import Logger

class FinanceModule:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("FinanceModule")
        
    def get_sales(self, email: str, password: str) -> list:
        return self.db_handler.fetch((email, password), "sales")
    
    def get_revenue(self, email: str, password: str) -> list:
        return self.db_handler.fetch((email, password), "revenue")