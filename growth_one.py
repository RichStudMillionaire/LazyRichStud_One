from objects import LogManager
from objects import TimeManager

class GrowthOne():
    def __init__(self, system_name):
        self.system_name = system_name
        self.system_online_bool = False
        self.log = LogManager(self.system_name)
        self.time_manager = TimeManager()
        
    def put_system_online(self):
        self.system_online_bool = True
        self.start_of_operations_epoch = self.time_manager.get_today_in_epoch()
        self.start_of_operations_readable = self.time_manager.make_unix_epoch_readable(self.start_of_operations_epoch)
        self.log.create_log_file() 
        self.log.new_paragraph(self.start_of_operations_readable)
        
        
        
        
        