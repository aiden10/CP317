
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
import pandas as pd
from datetime import timedelta, datetime

class FinanceModule:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.report_generator = ReportGenerator()
        self.logger = Logger("FinanceModule")
    
    def get_sales(self, email: str) -> list:
        return self.db_handler.fetch_table(Sales)
    
    def get_sales_report(self, email: str) -> dict:
        # Email unused because not every email has sales data
        # For testing, we'll just show the sales data of the entire sales table.
        sales_data = self.db_handler.fetch_table(Sales)
        return {
                "chart": self.report_generator.generate_sales_graph(sales_data),
                "insight": self.get_insight(sales_data),
                "income_notes": self.get_income_notes(sales_data),
            }

    def get_insight(self, sales_data: list) -> str:
        """
        Analyzes sales data to provide a meaningful insight about trends or statistics.
        :param sales_data: list of dictionaries containing sales data
        :return insight: a string which shows some trend or interesting statistic
        """
        
        # Return empty string if no data
        if not sales_data or len(sales_data) == 0:
            return "Insufficient data to generate insights."
        
        # Convert sales data to DataFrame
        df = pd.DataFrame(sales_data)
        
        # Identify key columns
        date_column = next((col for col in ['date', 'Date', 'sale_date', 'order_date'] if col in df.columns), None)
        price_column = next((col for col in ['price', 'Price', 'unit_price'] if col in df.columns), None)
        quantity_column = next((col for col in ['quantity', 'Quantity', 'qty'] if col in df.columns), None)
        department_column = next((col for col in ['department', 'Department', 'category'] if col in df.columns), None)
        item_column = next((col for col in ['item', 'Item', 'product', 'product_name'] if col in df.columns), None)
        
        # Handle missing columns
        if date_column is None or price_column is None or quantity_column is None:
            return "Unable to generate insights due to missing required data fields."
        
        if date_column in df.columns and isinstance(df[date_column].iloc[0], str):
            df[date_column] = pd.to_datetime(df[date_column])
        
        # Calculate revenue
        df['revenue'] = df[price_column] * df[quantity_column]
        
        # Generate different types of insights based on available data
        insights = []
        
        try:
            # 1. Compare recent sales to overall average
            if date_column in df.columns:
                # Get the most recent date in the dataset
                latest_date = df[date_column].max()
                
                # Calculate days to look back for "recent" sales
                if len(df) > 30:
                    recent_period = 7  # Use a week for larger datasets
                else:
                    recent_period = max(1, len(df) // 5)  # Flexible for smaller datasets
                    
                recent_cutoff = latest_date - timedelta(days=recent_period)
                recent_sales = df[df[date_column] >= recent_cutoff]['revenue'].sum()
                avg_daily_recent = recent_sales / recent_period
                
                # Calculate overall daily average
                earliest_date = df[date_column].min()
                total_days = (latest_date - earliest_date).days + 1
                overall_avg_daily = df['revenue'].sum() / max(1, total_days)
                
                if avg_daily_recent > overall_avg_daily * 1.2:
                    percent_increase = ((avg_daily_recent / overall_avg_daily) - 1) * 100
                    insights.append(f"Recent sales are {percent_increase:.1f}% higher than the overall average.")
                elif avg_daily_recent < overall_avg_daily * 0.8:
                    percent_decrease = ((overall_avg_daily / avg_daily_recent) - 1) * 100
                    insights.append(f"Recent sales are {percent_decrease:.1f}% lower than the overall average.")
            
            # 2. Department or category insights
            if department_column in df.columns:
                # Average purchase value by department
                dept_avg = df.groupby(department_column).agg(
                    avg_value=('revenue', 'mean'),
                    total_sales=('revenue', 'sum'),
                    transaction_count=(price_column, 'count')
                ).sort_values('avg_value', ascending=False)
                
                if not dept_avg.empty:
                    top_dept = dept_avg.index[0]
                    top_dept_avg = dept_avg.iloc[0]['avg_value']
                    insights.append(f"Customers spend an average of ${top_dept_avg:.2f} on {top_dept} products.")
                    
                    # Find department with highest revenue per transaction
                    if len(dept_avg) > 1:
                        highest_value_dept = dept_avg.index[0]
                        lowest_value_dept = dept_avg.index[-1]
                        highest_value = dept_avg.iloc[0]['avg_value']
                        lowest_value = dept_avg.iloc[-1]['avg_value']
                        
                        if highest_value > 2 * lowest_value:
                            insights.append(f"{highest_value_dept} transactions average ${highest_value:.2f}, which is {(highest_value/lowest_value):.1f}x higher than {lowest_value_dept} at ${lowest_value:.2f}.")
            
            # 3. Product-specific insights
            if item_column in df.columns:
                # Most popular product by quantity
                product_qty = df.groupby(item_column)[quantity_column].sum().sort_values(ascending=False)
                if not product_qty.empty:
                    top_product = product_qty.index[0]
                    top_product_qty = product_qty.iloc[0]
                    total_qty = df[quantity_column].sum()
                    percentage = (top_product_qty / total_qty) * 100
                    
                    if percentage > 15:  # Only show if it's a significant portion
                        insights.append(f"{top_product} is the most popular item, representing {percentage:.1f}% of all units sold.")
                
                # Most profitable product
                product_revenue = df.groupby(item_column)['revenue'].sum().sort_values(ascending=False)
                if not product_revenue.empty:
                    top_revenue_product = product_revenue.index[0]
                    top_revenue = product_revenue.iloc[0]
                    total_revenue = df['revenue'].sum()
                    rev_percentage = (top_revenue / total_revenue) * 100
                    
                    if rev_percentage > 15:  # Only show if it's a significant portion
                        insights.append(f"{top_revenue_product} generates ${top_revenue:.2f} in sales, accounting for {rev_percentage:.1f}% of total revenue.")
            
            # 4. Day of week insights
            if date_column in df.columns:
                df['day_of_week'] = df[date_column].dt.day_name()
                day_sales = df.groupby('day_of_week')['revenue'].mean().sort_values(ascending=False)
                
                if len(day_sales) > 1:
                    best_day = day_sales.index[0]
                    worst_day = day_sales.index[-1]
                    best_day_sales = day_sales.iloc[0]
                    worst_day_sales = day_sales.iloc[-1]
                    difference = ((best_day_sales / worst_day_sales) - 1) * 100
                    
                    if difference > 30:  # Only show if there's a significant difference
                        insights.append(f"{best_day} is the best sales day, averaging ${best_day_sales:.2f}, which is {difference:.1f}% higher than {worst_day}.")
        
        except Exception as e:
            self.logger.write_log(f"Error generating insights: {e}")
            
            try:
                avg_transaction = df['revenue'].mean()
                insights.append(f"Average transaction value is ${avg_transaction:.2f}.")
            except:
                pass
                
            try:
                if len(df) > 10:
                    insights.append(f"Database contains {len(df)} sales transactions to analyze.")
            except:
                pass
        
        # Select the most interesting insight to return
        if insights:
            # Prioritize insights about trends or significant differences
            for insight in insights:
                if "higher than" in insight or "lower than" in insight or "%" in insight:
                    return insight
            # Otherwise return the first available insight
            return insights[0]
        
        return "No insights available"

    def get_income_notes(self, sales_data: list) -> list[str]:
        """
        Analyzes sales data to provide income statistics over different time periods.
        :param sales_data: list of dictionaries containing sales data
        :return notes: a list of strings detailing how much money was made over a period of time
        """
        import pandas as pd
        from datetime import datetime, timedelta
        
        # Return empty list if no data
        if not sales_data or len(sales_data) == 0:
            return ["No sales data available"]
        
        # Convert sales data to DataFrame
        df = pd.DataFrame(sales_data)
        
        # Identify key columns
        date_column = next((col for col in ['date', 'Date', 'sale_date', 'order_date'] if col in df.columns), None)
        price_column = next((col for col in ['price', 'Price', 'unit_price'] if col in df.columns), None)
        quantity_column = next((col for col in ['quantity', 'Quantity', 'qty'] if col in df.columns), None)
        
        # Calculate revenue if possible
        if price_column is not None and quantity_column is not None:
            df['revenue'] = df[price_column] * df[quantity_column]
        else:
            # If we don't have both price and quantity, try to use just price
            if price_column is not None:
                df['revenue'] = df[price_column]
            else:
                return ["Unable to calculate revenue due to missing price or quantity data"]
        
        notes = []
        
        # Total sales
        total_sales = df['revenue'].sum()
        notes.append(f"Sales Total: ${total_sales:,.2f}")
        
        # Time-based analysis if date column exists
        if date_column in df.columns:
            # Ensure date is in datetime format
            if isinstance(df[date_column].iloc[0], str):
                df[date_column] = pd.to_datetime(df[date_column])
            
            # Get the date range
            latest_date = df[date_column].max()
            earliest_date = df[date_column].min()
            
            today = datetime.now().date()
            
            # Handle datetime vs date comparison
            latest_date_normalized = latest_date.date() if hasattr(latest_date, 'date') else latest_date
            
            if latest_date_normalized == today:
                # Filter data for today's sales
                if hasattr(latest_date, 'date'):
                    # If latest_date is a datetime object
                    today_sales = df[df[date_column].dt.date == today]['revenue'].sum()
                else:
                    # If latest_date is already a date object
                    today_sales = df[df[date_column] == today]['revenue'].sum()
                notes.append(f"Sales Today: ${today_sales:,.2f}")
            
            # Calculate yesterday's sales
            yesterday = today - timedelta(days=1)
            
            # Check if we have data for yesterday
            has_yesterday_data = False
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                has_yesterday_data = (df[date_column].dt.date == yesterday).any()
                if has_yesterday_data:
                    yesterday_sales = df[df[date_column].dt.date == yesterday]['revenue'].sum()
            else:
                # If dates are already date objects
                has_yesterday_data = (df[date_column] == yesterday).any()
                if has_yesterday_data:
                    yesterday_sales = df[df[date_column] == yesterday]['revenue'].sum()
            
            if has_yesterday_data:
                notes.append(f"Sales Yesterday: ${yesterday_sales:,.2f}")
            
            # This week's sales (current week)
            week_start = today - timedelta(days=today.weekday())
            
            # Handle datetime vs date comparison for week calculations
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                week_mask = df[date_column].dt.date >= week_start
            else:
                # If dates are already date objects
                week_mask = df[date_column] >= week_start
            
            if week_mask.any():
                week_sales = df[week_mask]['revenue'].sum()
                notes.append(f"Sales This Week: ${week_sales:,.2f}")
            
            # Last week's sales
            last_week_start = week_start - timedelta(days=7)
            last_week_end = week_start - timedelta(days=1)
            
            # Handle datetime vs date comparison for last week
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                last_week_mask = (df[date_column].dt.date >= last_week_start) & (df[date_column].dt.date <= last_week_end)
            else:
                # If dates are already date objects
                last_week_mask = (df[date_column] >= last_week_start) & (df[date_column] <= last_week_end)
            
            if last_week_mask.any():
                last_week_sales = df[last_week_mask]['revenue'].sum()
                notes.append(f"Sales Last Week: ${last_week_sales:,.2f}")
            
            # This month's sales
            month_start = today.replace(day=1)
            
            # Handle datetime vs date comparison for month calculations
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                month_mask = df[date_column].dt.date >= month_start
            else:
                # If dates are already date objects
                month_mask = df[date_column] >= month_start
            
            if month_mask.any():
                month_sales = df[month_mask]['revenue'].sum()
                notes.append(f"Sales This Month: ${month_sales:,.2f}")
            
            # Last month's sales
            last_month_end = month_start - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            
            # Handle datetime vs date comparison for last month
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                last_month_mask = (df[date_column].dt.date >= last_month_start) & (df[date_column].dt.date <= last_month_end)
            else:
                # If dates are already date objects
                last_month_mask = (df[date_column] >= last_month_start) & (df[date_column] <= last_month_end)
            
            if last_month_mask.any():
                last_month_sales = df[last_month_mask]['revenue'].sum()
                notes.append(f"Sales Last Month: ${last_month_sales:,.2f}")
            
            # This quarter's sales
            current_quarter = (today.month - 1) // 3 + 1
            quarter_month = 3 * current_quarter - 2
            quarter_start = datetime(today.year, quarter_month, 1).date()
            
            # Handle datetime vs date comparison for quarter calculations
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                quarter_mask = df[date_column].dt.date >= quarter_start
            else:
                # If dates are already date objects
                quarter_mask = df[date_column] >= quarter_start
            
            if quarter_mask.any():
                quarter_sales = df[quarter_mask]['revenue'].sum()
                notes.append(f"Sales This Quarter: ${quarter_sales:,.2f}")
            
            # This year's sales
            year_start = datetime(today.year, 1, 1).date()
            
            # Handle datetime vs date comparison for year calculations
            if hasattr(df[date_column].iloc[0], 'date'):
                # If dates are datetime objects
                year_mask = df[date_column].dt.date >= year_start
            else:
                # If dates are already date objects
                year_mask = df[date_column] >= year_start
            
            if year_mask.any():
                year_sales = df[year_mask]['revenue'].sum()
                notes.append(f"Sales This Year: ${year_sales:,.2f}")
            
            # Average sales per day
            if hasattr(latest_date, 'date') and hasattr(earliest_date, 'date'):
                # If they are datetime objects
                days_span = max(1, (latest_date.date() - earliest_date.date()).days + 1)
            else:
                # If they are already date objects
                days_span = max(1, (latest_date - earliest_date).days + 1)
                
            avg_daily = total_sales / days_span
            notes.append(f"Average Daily Sales: ${avg_daily:,.2f}")
        
        # If we have few time-based notes, add some more general statistics
        if len(notes) < 3:
            # Average transaction value
            avg_transaction = df['revenue'].mean()
            notes.append(f"Average Transaction: ${avg_transaction:,.2f}")
            
            # Highest transaction
            max_transaction = df['revenue'].max()
            notes.append(f"Highest Transaction: ${max_transaction:,.2f}")
        
        return notes
    
    def get_revenue(self, email: str) -> list:
        return self.db_handler.fetch(Revenue, {"user": email})
