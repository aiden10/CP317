
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
        
    def get_sales(self, email: str) -> list:
        return self.db_handler.fetch((email), "sales", "owner_email")
    
    def get_revenue(self, email: str) -> list:
        return self.db_handler.fetch((email), "revenue", "owner_email")