
import PySimpleGUI as sg

class Widgets_menu():
    
    def __init__(self):
        
        self.layout = []

    def return_tab(self, context):
        
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


    def tab_layout(self, context):
        
        tabs = []
        for tab in context:
            
            tabs.append(
                self.return_tab(tab)
                )
        
        self.layout = [
            [sg.Text('Good day!\nSelect a tab.')],
            [sg.TabGroup([tabs],
                         tab_location='centertop',
                         #title_color='White', 
                         #tab_background_color='Black', 
                         #selected_title_color='Green', 
                         #selected_background_color='Gray', 
                         border_width=5),
             ],
            sg.Button('Exit')
            ]
        
    def join_widgets(self):
        
        widgets = self.layout
        
        return widgets

