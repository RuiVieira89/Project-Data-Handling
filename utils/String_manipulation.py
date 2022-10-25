
import os

def WinFolder_path_to_PY(windows_path):
    # This turns Win path \ into python \\
    ## do not forget to input a --> r'string' ##
    
    path_split = windows_path.split('\\')
    PY_path = os.path.join("/", "c:", os.sep, *path_split[1:])
    
    return PY_path
