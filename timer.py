import pandas as pd
import time
import numpy as np

class TimeFollow():
    
    def __init__(self, 
        days_seconds = 1, months_days = 10, years_months = 8,
        days = 1, months = 1, years = 1
    ):
        
        self.days_seconds = days_seconds
        self.months_days = months_days
        self.years_months = years_months
        self.days = days
        self.months = months
        self.years = years
        
    def schedule(self):
        
        time.sleep(self.days_seconds)             # wait for a day                       
        self.days = self.days + 1
        new_year = False
        
        if self.days > self.months_days:
            self.months = self.months + 1
            self.days = 1
        
        if self.months > self.years_months:
            self.years = self.years + 1
            self.months = 1
            new_year = True
            
        earth_time = f"{self.years}:{self.months}:{self.days}"        
        print(f"\ncurrent time: {earth_time}")
        
        return self.years, self.months, self.days, new_year       
