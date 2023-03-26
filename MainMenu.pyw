import sys
import subprocess
#import tkinter as tk

filename = sys.argv[1]

try:
    subprocess.check_call(["python", filename])
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)

""""
from MainMenu import TabsApp
import json

if __name__ == '__main__':
    root = tk.Tk()
    with open("config_widgets.json") as f:
        widget_config = json.load(f)
    with open("config_gen.json") as f:
        gen_config = json.load(f)
    app = TabsApp(root, widget_config, gen_config)
    root.mainloop()
""""