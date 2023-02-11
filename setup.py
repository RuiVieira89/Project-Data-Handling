
import importlib
import subprocess
import sys

import ast
import os

print('Running Setup.py')
print('Cleaning...')

## Clean cache
for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()
for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()
print('Cleaning cache: Done.')


def get_imported_modules(folder):
    # finds modules inside folder
    imported_modules = set()
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    code = f.read()
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for name in node.names:
                                imported_modules.add(name.name)
                        elif isinstance(node, ast.ImportFrom):
                            imported_modules.add(node.module)
    return imported_modules


def import_or_install_module(module_name):
    # function to install modules
    try:
        importlib.import_module(module_name)
        print(f"{module_name} is already installed.")
    except ImportError:
        print(f"{module_name} not found, installing it now.")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", module_name])
            print(f"{module_name} has been installed.")
        except ModuleNotFoundError:
            print(f"Error:{module_name} is not found.")


def main():

    modules = get_imported_modules(os.getcwd())
    ## install packages
    for module in modules:
        import_or_install_module(module)
    
    print('main(): All done.')

if __name__ == "__main__":

    main()

    print('End.')