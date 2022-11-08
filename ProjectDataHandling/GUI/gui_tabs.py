"""
Example:
This is not generalized
"""

# --> create new work pkg etc...

import PySimpleGUI as sg
import os

def GUI_tabs(context):

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
                
                element = [sg.Text(context["Child"][index]["commment"]),
                           sg.Button(context["Child"][index]["tile_name"])
                           ]
                elements.append(element)
            #elements = elements[0]

        return sg.Tab(context['tile_name'], elements, 
                        #title_color='Red', 
                        #background_color='Green', 
                        tooltip=context["commment"], 
                        element_justification= 'right')
                
    tabs = []
    for tab in context:
        tabs.append(return_tab(tab))
    
    tab_group = [[sg.Text('Good day!\nSelect a tab.')],
                 [sg.TabGroup([tabs],
                        tab_location='centertop',
                        #title_color='White', 
                        #tab_background_color='Black', 
                        #selected_title_color='Green', 
                        #selected_background_color='Gray', 
                        border_width=5), 
                  sg.Button('Exit')
                  ]]
    
    return tab_group
