
## Clean cache
for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()
for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()
print('Cleaning cache: Done.')

## install packages

import os

try:
    import numpy as np
except ModuleNotFoundError:
    os.system('pip install numpy')

try:
    import matplotlib as np
except ModuleNotFoundError:
    os.system('pip install matplotlib')

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    os.system('pip install PySimpleGUI')

try:
    import kaleido
except ModuleNotFoundError:
    os.system('pip install -U kaleido')

try:
    import plotly
except ModuleNotFoundError:
    os.system('pip install plotly')

try:
    import cv2
except ModuleNotFoundError:
    os.system('pip install opencv-python')

print('End.')