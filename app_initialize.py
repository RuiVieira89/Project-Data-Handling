import os

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    os.system('pip install PySimpleGUI')
import sys

from ProjectDataHandling.GUI.gui_tabs import GUI_tabs
from ProjectDataHandling.work_flow_automation.organize_folder import CreateFileSystem
from ProjectDataHandling.project_management.timelines.make_schedule_from_excel import Gantt_Schedule
from ProjectDataHandling.utils.String_manipulation import WinFolder_path_to_PY

def start_app(context, folder_json_file):
    
    sg.theme('BlueMono')

    tab_group = GUI_tabs(context)
        
    
    window = sg.Window("Tabs",tab_group)


    while True:
        event, values = window.read()
        print(f'event={event}') ## this is what matters
        print(f'values={values}')
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "folder creation":
            target_folder = sg.popup_get_folder('Select target folder',no_window=True)
            
            if target_folder != '':
                CreateFileSystem(target_folder, folder_json_file)
                sg.popup_ok(f'Folders created! \nFind them at: {target_folder}')
                
        elif event == "Schedule":
            target_folder = sg.popup_get_folder('Select target folder',no_window=True)
            if target_folder != '':
                gantt = Gantt_Schedule(
                    WinFolder_path_to_PY(target_folder))
                #text1 = sg.popup_get_text('Small : ')
                gantt.plot(7)
                gantt.gridlines('Month',30)
                gantt.today_line()
                gantt.ouput(show=True)
                sg.popup_ok(f'Schedule done! \nFind it at: {target_folder}')

    sg.popup_no_buttons('Have a nice day!', 
                        background_color='Black', 
                        text_color='white', 
                        auto_close_duration=2, 
                        auto_close=True, no_titlebar=True)

    window.close()

    
if __name__ == '__main__':
    exit(0)
    start_app()
