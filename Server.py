"""
Uses: 
    - RequestHandler
    - Logger
Called From:
    - Main

"""


from RequestHandler import RequestHandler

"""
This file should be the one which contains the server endpoints and calls the respective RequestHandler functions for each one.
We should also have endpoints for each of the following pages:
    - Dashboard
    - Sales
    - Revenue
    - Employees
    - Inventory
"""

class Server:
    def __init__(self):
        self.request_handler = RequestHandler()