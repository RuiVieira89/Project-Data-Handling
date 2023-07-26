
import os
import ast
import subprocess

def find_python_files(folder):
    python_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    tree = ast.parse(content)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.add(f"{node.module}.{alias.name}")
    
    return imports

def install_packages(imports):
    for package in imports:
        try:
            subprocess.run(["pip", "install", package], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")

def main():

    print('Running Setup.py')
    root_folder = os.getcwd()  
    all_imports = set()

    python_files = find_python_files(root_folder)

    for file_path in python_files:
        imports = extract_imports(file_path)
        all_imports.update(imports)

    print("Found the following imports:")
    for package in all_imports:
        print(package)

    install_packages(all_imports)

    
    print('Cleaning...')

    ## Clean cache
    for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()
    for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()
    print('Cleaning cache: Done.')



if __name__ == "__main__":
    main()
