
import json
import os

class CreateFileSystem:
    
    def __init__(self, target_folder, json_file):
        self.target_folder = target_folder
        self.folder_list = []
    
        with open(json_file, 'r', encoding="utf8") as f:
            jsonData = json.load(f)

        self.conditional_recursive_get_folders(
            jsonData["Folder_structure"]["Folders"])
            
        for folder in self.folder_list:
            os.mkdir(folder)
            
                
    def conditional_recursive_get_folders(self,data):
        #jsonData["Folder_structure"]["Folders"][0]["folder_name"]

        for i in range(len(data)):
          
            try: # check if it has cild folder
                data[i]["child_folders"]
            except Exception:
                condition = False
            else:
                condition = True

            if data[i]["level"] == 0: # 0th level folder (not sub-folder)
                folder = ''.join([self.target_folder, "\\", data[i]['folder_name']])

            else: # it a subfolder of the previous folder
                # get relative path
                relative_path = self.folder_list[-1].replace(self.target_folder, '') 
                # [1:] is to exclude empty element
                relative_path_split = relative_path.split('\\')[1:] 
                # get relevant relative path
                relative_path_os = relative_path_split[:data[i]["level"]]

                # folder path - used * operator to unpack list
                folder = os.path.join(*list([self.target_folder, *relative_path_os, 
                                       data[i]['folder_name']]))

            self.folder_list.append(folder)
            if condition:
                self.conditional_recursive_get_folders(data[i]['child_folders'])
