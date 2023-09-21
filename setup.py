from cx_Freeze import setup, Executable

base = None    

executables = [Executable("./src/fabricator.py", base=base)]

packages = ["sys", "os", "re", "warnings"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "fabricator",
    options = options,
    version = "1.0.0",
    description = 'Generador de clases PSR-4',
    executables = executables
)