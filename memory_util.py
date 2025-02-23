import os
import json

class HardDrive:
    def __init__(self):
        self.list = {}
        self.json_string = ""
        
        
    def convert_dict_to_json_string(self):
        self.json_string = json.dumps(self.dict)
        
    def save(self, dict, file_name):
        self.dict = dict
        self.convert_dict_to_json_string()
        
        with open(file_name, 'w') as file:
            file.write(self.json_string)
            
    def load(self, file_name):
        try:    
            with open(file_name,'r') as file:
                self.dict = json.load(file)
                return self.dict
        except Exception as e:
            print(e)
            return False
        
    def format(self, file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)