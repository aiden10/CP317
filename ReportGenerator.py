
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

    
    def generate_graph(report_data : dict, database_table : string) -> plt.figure:
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
            figure - a figure/graph representing a set of data (Figure)
        -------------------------------------------------------
        """

        # Determine a list of values in columns A and B
        column_titles = report_data.values # Determine columns to select in database

        # Determine array
        item_column = column_titles[0] # Name of column in database with items
        count_column = column_titles[1] # Name of column in database with revenue or count of items


        # Fill arrays with data from both columns in the database
        query_statement = "SELECT " + item_column + " FROM " + database_table
        mycursor.execute(query_statement)

        items = mycursor.fetchall() # Fetch recently executed query
        items = list(zip(*items)) # Convert query of data into a list/array of items


        query_statement = "SELECT " + count_column + " FROM " + database_table
        mycursor.execute(query_statement)

        item_counts = mycursor.fetchall()
        item_counts = list(zip(*item_counts))


        # Generate Graph
        figure = plt.figure
        axes = figure.add_subplot(1, 1, 1)
        axes.bar(
            range(len(items)), # Count of items for x-axis
            item_counts, # Revenue or stock of items for y-axis
            tick_label=items # Labelling each bar under the x-axis with item names
        )
        
        return figure
    
        """
        -------------------------------------------------------
        Function: generate_graph
        -------------------------------------------------------
        Assmptions: report_data is a dictionary variable filled
        with two strings. The first string contains the column
        name of items from the database and the second contains
        the second column name of the table being either "Revenue"
        or "Stock". database_table is the table name in the database
        to select. Using these parameters, the program will
        execute query statements to gather this data into two
        arrays which will then be plotted onto a bar graph.
        -------------------------------------------------------
        """
    
