import pandas as pd

import ProjectDataHandling.utils.String_manipulation as util

import ProjectDataHandling.project_management.timelines.make_schedule_from_excel as Gantt
import ProjectDataHandling.project_management.KPI_calc.Finance as Fin
import ProjectDataHandling.data_analysis.charts as Chart

import tkinter as tk
import pandas as pd
from tkinter import ttk


class GUIInterface:
    def __init__(self, button_list, comment_df):
        self.button_list = button_list
        self.comment_df = comment_df
        self.root = tk.Tk()
        self.root.title("My GUI")
        
        # Create tabs
        self.tab_control = tk.ttk.Notebook(self.root)
        self.tabs = {}
        for tab_name in comment_df['Tabs'].unique():
            self.tabs[tab_name] = tk.Frame(self.tab_control)
            self.tab_control.add(self.tabs[tab_name], text=tab_name)
        self.tab_control.pack(expand=1, fill="both")
        
        # Create buttons
        self.buttons = {}
        for button_name, button_func in button_list:
            button_tab = comment_df.loc[comment_df['Names'] == button_name, 'Tabs'].values[0]
            button_comment = comment_df.loc[comment_df['Names'] == button_name, 'Comments'].values[0]
            self.buttons[button_name] = tk.Button(self.tabs[button_tab], text=button_name)
            self.buttons[button_name].bind("<Enter>", lambda event, comment=button_comment: self.show_comment(comment))
            self.buttons[button_name].bind("<Leave>", lambda event: self.hide_comment())
            self.buttons[button_name].config(command=lambda func=button_func: self.button_clicked(func))
            self.buttons[button_name].pack()
    
    def show_comment(self, comment):
        self.comment_label = tk.Label(text=comment)
        self.comment_label.pack()
        
    def hide_comment(self):
        self.comment_label.pack_forget()
    
    def button_clicked(self, func):
        func(True)
    
    def run(self):
        self.root.mainloop()

"""
buttons_list = [("Button 1", button_1_command), ("Button 2", button_2_command), ...]
comments_df = pd.DataFrame({'Button': ['Button 1', 'Button 2', ...],
"""               


def main():

    names = []
    tabs = []
    comments = []

    objs = []
    obj_list = []

    objs.append(util.get_functions(Gantt))
    objs.append(util.get_functions(Fin))
    objs.append(util.get_functions(Chart))

    for import_ in objs:
        for obj in import_:
            names.append(obj[1]().name)
            tabs.append(obj[1]().tab)
            comments.append(obj[1]().comment)
            obj_list.append([obj[1]().name, obj[1]])

    d = {'Names': names, 'Tabs': tabs, 'Comments': comments}
    GUIfunctionality = pd.DataFrame(data=d)

    gui = GUIInterface(obj_list, GUIfunctionality)
    gui.run()
    
    
    # obj_list[0][1](run=True)
    print(obj_list)
    print(GUIfunctionality)
    


if __name__ == '__main__':

    main()


""""
PROMPT:

Create a GUI interface class using python library tkinter. 
The GUI will have tabs and buttons. 
When you hover the mouse on a button the GUI must show the comments. 
The class will take as inputs a python list and a pandas dataframe. 
The python list will have the button name in the first column and the 
object that that will be called when the button is pressed in the second column. 
The pandas dataframe will have the button name in the first column, the button 
tab in the second column, and the comments in the third column.


"""