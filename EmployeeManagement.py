
"""
Uses: 
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

"""
        
from DatabaseHandler import DatabaseHandler
from Logger import Logger
from Tables import Employees

class EmployeeManagement:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("EmployeeManagement")

    def get_employees(self) -> list:
        
        return self.db_handler.fetch_table(Employees)

    def add_employee(self, employee_id: int, first_name: str, last_name: str, position: str, pay: float, weekly_hours: float = 0.0) -> bool:
    
        employee = Employees(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            position=position,
            pay=pay,
            weekly_hours=weekly_hours
            
            )
        return self.db_handler.insert(employee)
        

    def get_employee_by_id(self, employee_id: int) -> dict:
        
        result = self.db_handler.fetch(Employees, {"employee_id": employee_id})
        return result if result else {}
        

    def update_employee(self, employee_id: int, position: str = None, pay: float = None, weekly_hours: float = None) -> bool:
        updates = {}
        if position is not None:
            updates["position"] = position
        if pay is not None:
            updates["pay"] = pay
        if weekly_hours is not None:
            updates["weekly_hours"] = weekly_hours
            

        if not updates:
            self.logger.write_log(f"No fields provided to update for employee ID: {employee_id}")
            return False

        return self.db_handler.update(Employees, {"employee_id": employee_id}, updates)
        

    def delete_employee(self, employee_id: int) -> bool:
            return self.db_handler.delete(Employees, {"employee_id": employee_id})
        

    def calculate_weekly_pay(self, employee_id: int) -> float:
    
        result = self.db_handler.fetch(Employees, {"employee_id": employee_id})
        if result and "pay" in result and "weekly_hours" in result:
            return result["pay"] * result["weekly_hours"]
        return 0.0
        

    def get_employee_hours(self) -> list:
        
        results = self.db_handler.fetch_table(Employees)
        if results:
            return [
                {
                    "employee_id": emp["employee_id"],
                    "first_name": emp["first_name"],
                    "last_name": emp["last_name"],
                    "weekly_hours": emp["weekly_hours"]
                    
                    
                }
                for emp in results
            ]
        return []           
