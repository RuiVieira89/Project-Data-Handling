import os

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    os.system('pip install PySimpleGUI')
import sys

from ProjectDataHandling.GUI.gui_tabs import GUI_tabs
from ProjectDataHandling.GUI.Chart_select_display import select_display

import ProjectDataHandling.data_analysis.distribution as dist

from ProjectDataHandling.work_flow_automation.organize_folder import CreateFileSystem

from ProjectDataHandling.project_management.timelines.make_schedule_from_excel import Gantt_Schedule
from ProjectDataHandling.project_management.KPI_calc.Finance import Cost_ratios

from ProjectDataHandling.utils.String_manipulation import WinFolder_path_to_PY
from ProjectDataHandling.utils.String_manipulation import get_functions

from ProjectDataHandling.dumpster_diving.select_use_excel_data import select_use_excel_data


def start_app(context, folder_json_file):
    
    try: # get external function
        import external_functions.functions as ext_funcs
        external_FLAG = True
        
        func_dict_external = get_functions(ext_funcs)
        
    except ModuleNotFoundError as e:
        print(f'No external functions found: {e}')
        external_FLAG = False
    
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
        
        elif event == "Visualization":
            
            func_dict = get_functions(dist)
            
            data = select_use_excel_data()
            select_display(func_dict, data)
        
        elif event == "Cost comparison":
            
            layout_cost = [ [sg.Text('EU cost:'), sg.InputText()],
                           [sg.Text('Overseas cost:'), sg.InputText()],
                           [sg.Text('EU logistics cost:'), sg.InputText()],
                           [sg.Text('Overseas logistics cost:'), sg.InputText()], 
                           [sg.Button('Ok'), sg.Button('Cancel')] ]

            window_cost = sg.Window("Window Title", layout_cost)
            event, values = window_cost.read()
            print(event, values)
            
            local_manufact_cost = float(values[0])
            overseas_manufact_cost = float(values[1])
            overseas_logistic_cost = float(values[3])
            local_logistic_cost = float(values[2])
            
            if event == "Ok":
                GUI_cost = Cost_ratios()
                CIM_cost = GUI_cost.CIM(local_manufact_cost, overseas_manufact_cost)
                CIL_cost = GUI_cost.CIL(local_manufact_cost, overseas_manufact_cost, 
                            overseas_logistic_cost, local_logistic_cost)
                
                sg.popup_ok(f'Cost Index Landing {CIM_cost} \nCost Index Manufacturing {CIL_cost}')
                window_cost.close()           
            
            elif event == 'Cancel':
                window_cost.close()
        
        elif external_FLAG:
            
            for name in func_dict_external:
                if name == event:
                    run_func = func_dict_external[name]
                    run_func()

    sg.popup_no_buttons('Have a nice day!', 
                        background_color='Black', 
                        text_color='white', 
                        auto_close_duration=2, 
                        auto_close=True, no_titlebar=True)

    window.close()

