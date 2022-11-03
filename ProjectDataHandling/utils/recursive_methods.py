

import json
import os

class Recursive_conditional:
    
    def __init__(self, json_data, condition_index):
        self.condition = condition_index
        self.list = []
    
        self.conditional_recursive(
            json_data)            
                
    def conditional_recursive(self,data):

        for i in range(len(data)):
          
            try: # Check condition
                data[i][self.condition]
            except Exception as e:
                condition = False
            else:
                condition = True

            if data[i]["level"] == 0: # 0th level 
                element = data[i]
                # do gui

            else: # sub-levels
                # get relevant level
                relative_path_os = element[:data[i]["level"]]
                # do gui 

            self.list.append(element)
            
            if condition:
                self.conditional_recursive(data[i][self.condition])
