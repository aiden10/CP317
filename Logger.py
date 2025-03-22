
"""
Uses:
    - None
    
Called From:
    - Every other module

"""
from datetime import datetime

class Logger:
    def __init__(self):
        pass
    
    def write_log(self, message: str, source: str) -> None:
        """
        Writes timestamped message to a log file
        """
        with open(f"{source}.log", "a", encoding="utf-8") as log_file:
            log_file.write(f'{datetime.now} | {message}')
        