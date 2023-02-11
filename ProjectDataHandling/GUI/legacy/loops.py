
import PySimpleGUI as sg

class Loop_tab():

    def __init__(self):
    
        try: # get external function
            import external_functions.functions as ext_funcs
            self.external_FLAG = True
            
            self.func_dict_external = get_functions(ext_funcs)
            
        except ModuleNotFoundError as e:
            print(f'No external functions found: {e}')
            self.external_FLAG = False
        
    def main_loop(self, window, modular_functions, conditions):
        
        while True:
            event, values = window.read()
            
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            else:
                for condition in conditions:
            
                    if event == condition:
                        
                        func[]
                        

