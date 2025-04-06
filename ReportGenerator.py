
"""
Uses: 
    - Logger

Called From:
    - DashboardSummarizer
    - FinanceModule (maybe)

This file should probably be the one generating graphs and maybe insights? But the insights feel like they could also go in the FinanceModule.
"""

import matplotlib.pyplot as plt
import string
from Logger import Logger

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost", # [CHANGE] Change this string to host of the database we are using 
    user = "username", # [CHANGE] Change this string to username database is using
    password = "password", # [CHANGE] Change this string to password database is using
    database = "database" # [CHANGE] Change this string to the name of the database we are using
)

mycursor = mydb.cursor()


class ReportGenerator:
    def __init__(self):
        """
        -------------------------------------------------------
        Initializes the ReportGenerator class.
        Use: ReportGenerator()
        -------------------------------------------------------
        Parameters:
            None
        Returns:
            None
        -------------------------------------------------------
        """
        self.logger = Logger()

    
    def generate_graph(report_data : dict) -> plt.figure:
        """
        -------------------------------------------------------
        Creates a graph based on the report data passed. The
        report_data contains a dictionary of strings that
        represents the column names in the database table.
        This function will locate the these columns in the
        database using report_data in order to generate a graph.
        Use: generate_graph(report_data)
        -------------------------------------------------------
        Parameters:
            report_data - a dictionary filled with strings (Dictionary)
        Returns:
            None
        -------------------------------------------------------
        """

        # Determine a list of values in columns A and B
        column_titles = report_data.values # Determine columns to select in database

        # Then SQL statements will be used here to gather data from table and insert data into the arrays below
        # query_statement =
        #
        #

        items = []
        item_counts = []

        # Generate Graph

        figure = plt.figure
        axes = figure.add_subplot(1, 1, 1)
        axes.bar(
            range(len(items)),
            item_counts,
            tick_label=items
        )
        
        return figure
    
