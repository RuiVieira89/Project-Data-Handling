"""
Example:
This is not generalized
"""


import PySimpleGUI as sg
from ProjectDataHandling.work_flow_automation.organize_folder import CreateFileSystem
from ProjectDataHandling.project_management.timelines.make_schedule_from_excel import Gantt_Schedule
from ProjectDataHandling.utils.String_manipulation import WinFolder_path_to_PY


def Resizable_Dashboard_using_Frames(tile_context, target_folder, folder_json_file):

    def return_frame(title):
        return [sg.Button(title, pad=(5, 3), 
                        expand_x=True, expand_y=True, 
                        #background_color='#404040', 
                        border_width=0)]
    
    def return_tab(context):
        
        elements = [
            [sg.Text(context['commment'])],
        ]
        
        try: # Check condition
            context["Child"]
        except Exception as e:
            condition = False
        else:
            condition = True
        
        if condition:
            elements = []
            for index in range(len(context["Child"])):
                
                element = [sg.Button(context["Child"][index]["tile_name"]),
                           #sg.Text(context['commment'])
                           ]
                elements.append(element)
            #elements = elements[0]

        return sg.Tab(context['tile_name'], elements, 
                        title_color='Red', background_color='Green', 
                        tooltip='Instructions', 
                        element_justification= 'right')
        
    tabs = []
    for tab in tile_context:
        tabs.append(return_tab(tab))
    
    tab_group = [[sg.TabGroup([tabs],
                        tab_location='centertop',
                        title_color='White', 
                        tab_background_color='Black', 
                        selected_title_color='Green', 
                        selected_background_color='Gray', 
                        border_width=5), 
                  sg.Button('Exit')
                  ]]
    
    window = sg.Window("Tabs",tab_group)


    while True:
        event, values = window.read()
        print(f'event={event}') ## this is what matters
        print(f'values={values}')
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "folder creation":
            target_folder = sg.popup_get_folder('Select target folder',no_window=True)
            CreateFileSystem(target_folder, folder_json_file)
            
        elif event == "Schedule":
            target_folder = sg.popup_get_folder('Select target folder',no_window=True)
            gantt = Gantt_Schedule(
                WinFolder_path_to_PY(target_folder))
            gantt.plot(7)
            gantt.gridlines('Month',30)
            gantt.ouput(show=True)

        
    window.close()

