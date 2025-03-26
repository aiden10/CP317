
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
import base64

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

    # Unsure if these should return strings or something else like an image or pdf
    def generate_report(self, report_data: dict) -> str:
        ...

    # Uses the email to know which data to fetch from the database
    def summarize_reports(self, email: str) -> dict:
        with open("dashboard/assets/chart.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Sample data, to be replaced with actual database data 
        return {
            "updates": ["Order 1 filled", "$4532 made in sales today", "Employee requested sick day"],
            "chart": encoded_image,
            "income_notes": ["328K Total Monthly Income", "55K Net Monthly Income"],
            "insight": "Your current monthly revenue is 40% higher than last month's"
        }