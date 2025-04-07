
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - DashboardSummarizer
"""

from DatabaseHandler import DatabaseHandler
from ReportGenerator import ReportGenerator
from Logger import Logger
from Tables import Sales, Revenue

class FinanceModule:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.report_generator = ReportGenerator()
        self.logger = Logger("FinanceModule")
        
    def get_sales(self, email: str) -> list:
        # return self.db_handler.fetch(Sales, {"user": email}) commented out because the sample data only exists for certain email addresses
        return self.db_handler.fetch_table(Sales)
    
    def get_sales_report(self, email: str) -> dict:
        sales_data = self.get_sales(email)
        return {
                "chart": self.report_generator.generate_sales_graph(sales_data),
                "insight": "tbd",
                "income_notes": ["tbd", "tbd", "tbd"],
            }
    
    def get_revenue(self, email: str) -> list:
        return self.db_handler.fetch(Revenue, {"user": email})
