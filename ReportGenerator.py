
"""
Uses: 
    - Logger
    - FinanceModule

Called From:
    - DashboardSummarizer
    - FinanceModule (maybe)

This file should probably be the one generating graphs and maybe insights? But the insights feel like they could also go in the FinanceModule.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
import pandas as pd
from Logger import Logger
from Tables import Sales
from FinanceModule import FinanceModule
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.logger = Logger("ReportGenerator")
        self.finance = FinanceModule()

    def generate_sales_report(self, email: str) -> dict:
        # Email unused because not every email has sales data
        # For testing, we'll just show the sales data of the entire sales table.
        sales_data = self.finance.get_sales(email)
        return {
                "chart": self.generate_sales_graph(sales_data),
                "insight": self.finance.get_insight(sales_data),
                "income_notes": self.finance.get_income_notes(sales_data),
            }

    def generate_revenue_report(self, email: str) -> dict:
        # Email unused because not every email has sales data
        # For testing, we'll just show the revenue data of the entire revenue table.
        revenue_data = self.finance.get_revenue(email)
        sales_data = self.finance.get_sales(email)

        return {
                "bar_chart": self.generate_revenue_bar_graph(revenue_data),
                "pie_chart": self.generate_revenue_pie_graph(revenue_data),
                "insight": self.finance.get_insight(sales_data),
                "income_notes": self.finance.get_income_notes(sales_data),
            }

    def generate_revenue_bar_graph(self, revenue_data: list) -> str:
        """
        Generates a bar graph based on revenue data. The graph shows weekly revenue.
        :param revenue_data: the revenue data used to generate the graph
        :return encoded_graph: the graph encoded as a string
        """
        df = pd.DataFrame(revenue_data)
        plt.style.use('dark_background')

        # Convert to datetime safely
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # Drop any invalid dates

        # Group by week starting Monday
        df['week'] = df['date'].dt.to_period('W-MON').apply(lambda r: r.start_time)

        weekly_revenue = df.groupby('week')['net_revenue'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(weekly_revenue['week'], weekly_revenue['net_revenue'], color='skyblue')
        ax.set_title('Weekly Net Revenue')
        ax.set_xlabel('Week')
        ax.set_ylabel('Net Revenue ($)')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)

        encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)

        return encoded_image

    def generate_revenue_pie_graph(self, revenue_data: list) -> str:
        """
        Generates a pie chart based on revenue data. The chart shows revenue by user.
        :param revenue_data: the revenue data used to generate the graph
        :return encoded_graph: the graph encoded as a string
        """
        df = pd.DataFrame(revenue_data)
        plt.style.use('dark_background')

        if 'user' not in df.columns or 'net_revenue' not in df.columns:
            raise ValueError("Data must contain 'user' and 'net_revenue' fields")

        revenue_by_user = df.groupby('user')['net_revenue'].sum().sort_values(ascending=False)
        revenue_by_user = revenue_by_user[revenue_by_user > 0]

        explode = [0.1] + [0 for _ in range(len(revenue_by_user) - 1)]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(revenue_by_user, labels=revenue_by_user.index, autopct='%1.1f%%',
            startangle=90, shadow=True, explode=explode)
        ax.set_title('Net Revenue by User')

        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)

        encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)

        return encoded_image

    def generate_sales_graph(self, sales_data: list) -> str:
        """
        Generates a graph based on sales data.
        :param sales_data: the sales data used to generate the graph
        :return encoded_graph: the graph encoded as a string
        """
        
        df = pd.DataFrame(sales_data)
        plt.style.use('dark_background')
        if isinstance(df['date'].iloc[0], str):
            df['date'] = pd.to_datetime(df['date'])
        
        df['revenue'] = df['quantity'] * df['price']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Sales Analytics', fontsize=16)
        
        daily_sales = df.groupby('date')['revenue'].sum().reset_index()
        axes[0, 0].plot(daily_sales['date'], daily_sales['revenue'], marker='o', linestyle='-', color='royalblue')
        axes[0, 0].set_title('Daily Sales Revenue')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Revenue ($)')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45)
        
        dept_sales = df.groupby('department')['revenue'].sum().sort_values(ascending=False)
        dept_sales.plot(kind='bar', ax=axes[0, 1], color='teal')
        axes[0, 1].set_title('Sales by Department')
        axes[0, 1].set_xlabel('Department')
        axes[0, 1].set_ylabel('Revenue ($)')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        top_items_qty = df.groupby('item')['quantity'].sum().sort_values(ascending=False).head(5)
        top_items_qty.plot(kind='barh', ax=axes[1, 0], color='green')
        axes[1, 0].set_title('Top 5 Products by Quantity Sold')
        axes[1, 0].set_xlabel('Quantity Sold')
        axes[1, 0].set_ylabel('Product')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        top_items_rev = df.groupby('item')['revenue'].sum().sort_values(ascending=False).head(5)
        explode = [0.1] + [0 for _ in range(len(top_items_rev)-1)]
        axes[1, 1].pie(top_items_rev, labels=top_items_rev.index, autopct='%1.1f%%', 
                    startangle=90, shadow=True, explode=explode)
        axes[1, 1].set_title('Top 5 Products by Revenue')
        
        plt.tight_layout()
        fig.subplots_adjust(top=0.9)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        
        encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
        
        plt.close(fig)
        
        return encoded_image
    
    
