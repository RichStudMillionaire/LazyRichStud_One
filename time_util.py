from datetime import datetime, date, timedelta
import time
import calendar

class Timestamp:
    def __init__(self):
        pass
    def now(self):
        return datetime.now()
    def today(self):
        return date.today()

class ChunkManager:
    def __init__(self, chunk_size, pause_time_in_seconds, ticker_list):
        self.chunk_size = chunk_size
        self.pause = pause_time_in_seconds
        self.list_length = len(ticker_list)
        self.total = 0
        self.count=0
    def tally_click(self):
        self.count+=1
        self.check_tally_and_pause()
    def check_tally_and_pause(self):
        if self.count == self.chunk_size:
            self.total+=self.count
            print("Zzz... Going to sleep for {} seconds".format(self.pause))
            print("Progress : {} tickers out of {}".format(self.total, self.list_length))
            time.sleep(self.pause)
            self.count = 0
            
class Timekeeper:
    def __init__(self):
        pass
    def set_datetime_object(self,yyyy, m, d, hours, minutes):
        return datetime(yyyy,m,d,hours, minutes)
    
    def get_minutes_passed_between_dates(self, most_recent_datetime, older_datetime):
        delta = most_recent_datetime - older_datetime
        minutes = delta.total_seconds()/60
        return int(minutes)
    def get_hours_passed_between_dates(self, most_recent_datetime, older_datetime):
        delta = most_recent_datetime - older_datetime
        hours = delta.total_seconds()/3600
        return int(hours)
    def get_days_passed_between_dates(self,most_recent_datetime, older_datetime):
        n=most_recent_datetime
        o=older_datetime
        hours = self.get_hours_passed_between_dates(n,o)
        return int(hours/24)
    def get_days_in_month(self, int_month):
        year = datetime.now().year
        nb_of_days = calendar.monthrange(year,int_month)
        return nb_of_days[1]
    def get_days_left_in_the_month(self):
        month=datetime.now().month
        day = datetime.now().day
        nb = self.get_days_in_month(month)
        left = nb-day
        return left
    def change_month(self, current):
        if current+1 == datetime.today().month:
            current = datetime.today().month
        return current