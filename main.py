import pandas as pd

import ProjectDataHandling.utils.String_manipulation as util

import ProjectDataHandling.project_management.timelines.make_schedule_from_excel as Gantt
import ProjectDataHandling.project_management.KPI_calc.Finance as Fin
import ProjectDataHandling.data_analysis.charts as Chart

import tkinter as tk
import pandas as pd
from tkinter import ttk


class GUI:
    def __init__(self, buttons_list, comments_df):
        self.root = tk.Tk()
        self.root.title("GUI Interface")
        self.root.geometry("500x500")
        self.tab_control = ttk.Notebook(self.root)
        self.buttons_list = buttons_list
        self.comments_df = comments_df

        self.create_tabs()
        self.create_buttons()

    def create_tabs(self):
        tabs = self.comments_df['Tabs'].unique()
        self.tab_dict = {}
        for tab in tabs:
            self.tab_dict[tab] = tk.Frame(self.tab_control)
            self.tab_control.add(self.tab_dict[tab], text=tab)
        self.tab_control.pack(expand=1, fill='both')

    def create_buttons(self):
        for button in self.buttons_list:
            button_name = button[0]
            button_command = button[1]
            button_tab = self.comments_df[self.comments_df['Names'] == button_name]['Tabs'].iloc[0]
            button_comment = self.comments_df[self.comments_df['Names'] == button_name]['Comments'].iloc[0]
            b = tk.Button(self.tab_dict[button_tab], text=button_name, command=button_command(run=True))
            b.pack()
            #b.bind("<Enter>", lambda event, b=b, c=button_comment: self.show_comments(event, b, c))
            #b.bind("<Leave>", lambda event, b=b: self.remove_comments(event, b))

    def show_comments(self, event, button, comments):
        self.tooltip = tk.Label(self.root, text=comments, background='white', relief='solid', borderwidth=1)
        self.tooltip.pack()
        self.tooltip.bind("<Leave>", lambda event, b=self.tooltip: self.remove_comments(event, b))
        self.tooltip.bind("<ButtonPress>", lambda event, b=self.tooltip: self.remove_comments(event, b))
        self.tooltip.place(x=event.x_root, y=event.y_root+20, height=100, width=100)

    def remove_comments(self, event, widget):
        widget.pack_forget()

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

    gui = GUI(obj_list, GUIfunctionality)
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