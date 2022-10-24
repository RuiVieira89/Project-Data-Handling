
import json
import os

class CreateFileSystem:
    
    def __init__(self):
        pass
    
    def conditional_recursive(data, condition):
        #jsonData["Folder_structure"]["Folders"][0]["folder_name"]
        
        

        pass
    
    def create_folder(target_folder):
        
        json_file = ''.join([os.getcwd(), 
                             "\\scripts_EDA\\work_flow_automation\\organize_folder.json"])
        with open(json_file, 'r') as f:
            jsonData = json.load(f)

        for x in jsonData:
            if x == 'folder_name':
                os.mkdir(target_folder + "\\" + jsonData[x])


