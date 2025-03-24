
"""
Uses:
    - AssetManagement
    - FinanceModule
    - Logger

Called From:
    - RequestHandler

"""

from FinanceModule import FinanceModule
from AssetManagement import AssetManagement
from Logger import Logger

class DashboardSummarizer:
    def __init__(self):
        self.assets = AssetManagement()
        self.finances = FinanceModule()
        self.logger = Logger("DashboardSummary")

    # Uses the email to know which data to fetch from the database
    def get_report_data(self, email: str) -> dict:
        return {
            "sales": self.finances.get_sales(email),
            "revenue": self.finances.get_revenue(email),
            "assets": self.assets.get_assets(email) # Not really sure what assets are, but it was listed in the diagram   
        }

    # Unsure if these should return strinsg or something else like an image or pdf
    def generate_report(report_data: dict) -> str:
        ...

    # Uses the email to know which data to fetch from the database
    def summarize_reports(email: str) -> str:
        ...