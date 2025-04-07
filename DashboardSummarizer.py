
"""
Uses:
    - AssetManagement
    - FinanceModule
    - Logger

Called From:
    - RequestHandler

"""
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
from FinanceModule import FinanceModule
from AssetManagement import AssetManagement
from datetime import datetime
from Logger import Logger
import base64

class DashboardSummarizer:
    def __init__(self):
        self.assets = AssetManagement()
        self.finances = FinanceModule()
        self.logger = Logger("DashboardSummary")

    # Unsure if these should return strings or something else like an image or pdf
    def generate_report(self, report_data: dict, file=None):
        file = "generate_report.pdf"

        curr_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

        c = canvas.Canvas(file, pagesize=letter)

        x = 100
        y = 750

        c.setFont("Helvetica-Bold", 24)
        c.drawString(x+ 100,y,"General Report")

        y -= 30
        c.setFont("Helvetica-Oblique", 14)

        #line format
        c.drawString(x + 20,y, f"Generated on: {curr_time}")
        y -=60

        c.setFont("Helvetica-Bold", 16)
        c.drawString(x,y,"Report Overview")

        c.setLineWidth(1)
        c.line(x,y- 10, x + 400, y - 10)


        y -= 30

        c.setFont("Helvetica", 14)

        for key, val in report_data.items(): 
            c.drawString(x,y,f"{key}: {val}")
            y -= 20

        p_width, p_height = letter
        c.drawString(p_width - 240 ,20,"Report Generated by GSFT Co.") #do this at the end

        c.save()

        return file

    # Uses the email to know which data to fetch from the database
    def summarize_reports(self, email: str) -> dict:
        with open("dashboard/assets/chart.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            #not sure how to use this

        income = []
        updates = [0]
        sales = 0

        income_notes = self.finances.get_revenue(email)
        insights_sales = self.finances.get_sales(email)

        if isinstance(insights_sales,dict):
            sales = insights_sales["price"]
            if insights_sales["date"] == datetime.now().date():
                updates[0] += insights_sales["price"]


        else:
            for i in insights_sales:
                sales += i["price"]
                if i["date"] == datetime.now().date():
                    updates[0] +=  i["price"]


        if income_notes:
            income.append(str(income_notes[-1]["total_sales"]) + " Total Monthly Income")
            income.append(str(income_notes[-1]["net_revenue"]) + " Net Monthly Income" )
            


        return {
            "updates": ["$" + str(updates[0]) + " made in sales today"], # will generate sales generated on current day 
            "chart": encoded_image,
            "income_notes": income,
            "insight": f"Your current monthly sales is up ${sales} currently"  #previous month revenue is not stored, so will generate how much $ spent on sales 
        }