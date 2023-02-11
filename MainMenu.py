
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import json

class TabsApp:
    def __init__(self, master, widget_config, gen_config):
        self.context = widget_config
        self.master = master
        self.master.title("Tabs Example")
        self.master.geometry(gen_config[0]["gen_config"][0]["size_config_geometry"])
        self.notebook = ttk.Notebook(self.master)
        self.tabs = {}
        for tab in widget_config:
            tab_frame = ttk.Frame(self.notebook)
            self.tabs[tab["name"]] = tab_frame
            self.notebook.add(tab_frame, text=tab["name"])
        self.notebook.grid(pady=10)
        for tab in widget_config:
            self.create_widgets(tab)
    
    def create_widgets(self, context):
        for widget in context['widgets']:
            for widget_type, widget_params in widget.items():
                if widget_type == 'Button':
                    button = tk.Button(
                        self.tabs[context["name"]], 
                        text=widget_params['text'], 
                        font=('Helvetica', 16),
                        bg='red', height=3, width=15,
                        command=lambda: TabsApp.show_window(
                            widget_params['command'], 
                            widget_params['text']
                        )
                    )
                    button.grid(row=widget_params['row'], 
                    column=widget_params['column'], 
                    pady=10, padx=10)
                    
    @classmethod
    def show_window(cls, title, message):
        messagebox.showinfo(title, message)

if __name__ == '__main__':
    root = tk.Tk()
    with open("config_widgets.json") as f:
        widget_config = json.load(f)
    with open("config_gen.json") as f:
        gen_config = json.load(f)
    app = TabsApp(root, widget_config, gen_config)
    root.mainloop()


exit (0)

class GUIEngine:
    def __init__(self, master, title, message):
        self.master = master
        self.master.title(title)
        self.master.geometry("400x400")
        self.label = tk.Label(self.master, text=message)
        self.label.pack(pady=10)
        self.close_button = tk.Button(self.master, text="Close", command=self.master.destroy)
        self.close_button.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = GUIEngine(root, "Sample GUI", "Welcome to the GUI")
    root.mainloop()


class MainMenu:
    def __init__(self, master, context):
        self.master = master
        self.context = context
        self.create_widgets()
        
    def create_widgets(self):
        for widget in self.context['widgets']:
            for widget_type, widget_params in widget.items():
                if widget_type == 'Button':
                    button = tk.Button(
                        self.master, 
                        text=widget_params['text'], 
                        font=('Helvetica', 16),
                        bg='red', height=3, width=15,
                        command=lambda: MainMenu.show_window(
                            widget_params['command'], 
                            widget_params['text']
                        )
                    )
                    
                    button.grid(row=widget_params['row'], 
                    column=widget_params['column'], 
                    pady=10, padx=10)
                    
    @classmethod
    def show_window(cls, title, message):
        messagebox.showinfo(title, message)
        
def run_app(file):
    with open(file) as f:
        context = json.load(f)
    root = tk.Tk()
    root['bg'] = 'white'
    root.title(context['MainMenu']['title'])
    app = MainMenu(root, context['MainMenu'])
    root.mainloop()



#run_app("Context_GUI.json")
