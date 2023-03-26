
def WinFolder_path_to_PY(windows_path):
    # This turns Win path \ into python \\
    ## do not forget to input a --> r'string' ##
    
    import os
    
    if len(windows_path.split('\\')) == 1:
        path_split = windows_path.split('/')
        PY_path = os.path.join("/", "c:", os.sep, *path_split[1:])
        
    else:
        
        try:
            path_split = windows_path.split('\\')
            PY_path = os.path.join("/", "c:", os.sep, *path_split[1:])
        except Exception:
            print('\ndo not forget to input r before string for RAW STRING\n')
            exit(0)
    
    return PY_path

def get_functions(module):
    
    from inspect import getmembers, isfunction, isclass

    funcs = getmembers(module, isfunction)
    classes = getmembers(module, isclass)

    member_dict = []
    for name_func, func in funcs:
        member_dict.append([name_func, func])

    for name_class, class_ in classes:
        member_dict.append([name_class, class_])

    return member_dict
