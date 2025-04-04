
"""
Uses:
    - None
    
Called From:
    - Every other module

"""
from datetime import datetime

class Logger:
    def __init__(self, source: str):
        self.source = source
    
    def write_log(self, message: str) -> None:
        """
        Writes timestamped message to a log file
        :param message: the string to log
        """
        with open(f"logs/{self.source}.log", "a", encoding="utf-8") as log_file:
            log_file.write(f'{datetime.now().strftime("%d|%m|%Y, %H:%M:%S")} | {message}\n')
        