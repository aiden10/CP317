
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - DashboardSummarizer
"""

from Logger import Logger
from DatabaseHandler import DatabaseHandler

class AssetManagement:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("AssetManagement")

    def get_assets(self, email: str, password: str) -> list:
        return self.db_handler.fetch_row((email, password), "assets")