#! /bin/env/python
import sys
import os
import re
import warnings

warnings.filterwarnings("ignore")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printHelp():
    print("╔══════════════════════════════════════════════════════╗");
    print("║               ", end="")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}fabricator  - V1.0.0                   ",  end="")
    print(f"{bcolors.ENDC}║")
    print("╟──────────────────────────────────────────────────────╢")
    print("║           ", end="")
    print(f"{bcolors.OKCYAN}{bcolors.BOLD}  a KCRAM SOLUTIONS' Technology            {bcolors.ENDC}║")
    print("╚══════════════════════════════════════════════════════╝")
    print("\nEsta herramienta permite crear clases PHP siguiendo el estandar PSR-4 que se usa en composer.\nCrea la clase en el directorio correspondiente")
    print(f"{bcolors.OKBLUE}Usage:")
    print(f"{bcolors.OKGREEN}  fabricator {bcolors.OKCYAN}[options] {bcolors.ENDC}<class_name>")
    print(f"\n{bcolors.OKCYAN}Options:")
    print(f"{bcolors.WARNING}   -n=<name>    {bcolors.ENDC}             Namespace a usar para la clase")
    print(f"{bcolors.WARNING}   -p=<ruta>    {bcolors.ENDC}             Ruta del archivo package.json por defecto se toma el directorio actual")
    print(f"{bcolors.WARNING}   -i           {bcolors.ENDC}             Indicamos que el namespace y la clase se proporcionan como un solo argumento")
    print(f"{bcolors.WARNING}   -d           {bcolors.ENDC}             Crea el directorio si no existe")
    print(f"{bcolors.WARNING}   -h           {bcolors.ENDC}             Muestra la ayuda")
    print(f"{bcolors.BOLD}\nEjemplos: {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}\tfabricator {bcolors.WARNING}-i -d {bcolors.ENDC} \\KcramSolutions\\Project\\Utils\\Constants")
    print()

def printError(msg, showHelp = True):
    print(f"❌{bcolors.BOLD} {bcolors.FAIL}Ha habido un error: \n\t{msg} {bcolors.ENDC}")
    print()
    if showHelp:
        printHelp()
    sys.exit(20)


def in_array(arr, val):
    '''
    Check if a option exists in args
    '''
    for item in arr:
        if item.startswith(f"-{val}"):
            return True
    return False

def extract_option_val(arr, option):
    if in_array(arr, option):
        for item in arr:
           
            if item.startswith(f"-{option}"):
                slices = item.split("=")
                if len(slices) == 2:
                    return slices[1].strip()
    return False

# MAIN SLICE -> program start::
args = sys.argv[1::]


try:
    if len(args) == 0:
        printHelp()
        sys.exit(1)

    createDirs = in_array(args, "d");
    optionsFile = in_array(args, "p")
    help = in_array(args, "h")
    packageDir = None
    nameSpace = None
    workDir = None
    className = args[-1];
    configData = {
        "namespace" : None,
        "path": None
    }


    if help:
        printHelp()
        sys.exit(0)

    if len(args) == 0:
        printError("No se han pasado argumentos");

    if optionsFile:
        packageDir = extract_option_val(args, "p")
        if not packageDir.endswith("composer.json"):
            printError(f"No se ha asignado un archivo valido como archivo composer json {packageDir}", False)
    else:
        packageDir = os.path.join(os.getcwd(), "composer.json")

    workDir = os.path.dirname(packageDir)

    print(f"✉️  Path del proyecto: {bcolors.UNDERLINE}{workDir}{bcolors.ENDC}")
    if in_array(args, "i"):
        if len(args) == 2 or \
        (len(args) == 3 and (createDirs or optionsFile)) or \
        (len(args) == 4 and createDirs and optionsFile):
            split = className.split("\\")
            className = split[-1].capitalize()
            split.pop()
            nameSpace = "\\".join(split) + "\\"
        else:
            printError("Faltan argumentos")
    elif in_array(args, "n"):
        nameSpace = extract_option_val(args, "n")
        className = className.capitalize()
    else:
        printError("Faltan argumentos")

    # LEEMOS LA CONFIGURACION
    if not os.path.isfile(packageDir):
        printError(f"No se ha encontrado el archivo {packageDir}", False)

    print(f"✌️  {bcolors.OKCYAN}Recuperando la configuración {bcolors.ENDC}")

    configFl = open(packageDir, "r")

    configStr = configFl.read()
    regex = r"\"psr-4\":\s+\{\s*\"(?P<namespace>.*)\"\s?:\s?\"(?P<ruta>.*)\",?$"
    matches = re.finditer(regex, configStr, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        configData["namespace"]= match.group(1).replace("\\\\", "\\")
        configData["path"]= match.group(2).replace("/", os.path.sep)

    if configData["namespace"] is None or configData["path"] is None:
        printError(f"No hemos podido procesar el archivo {packageDir}", False)

    if not nameSpace.startswith(configData["namespace"]):
        projectName = configData["namespace"]
        printError(f"No coinciden los namespace:\n\t  Namespace pasado: {nameSpace}\n\t  Namespace del proyecto: {projectName}", False)

    sizeOfPNS =len(configData["namespace"]);
    finalDir = os.path.join(workDir, configData["path"])
    if sizeOfPNS != len(nameSpace):
        directory =  nameSpace[sizeOfPNS::]
        finalDir = os.path.join(finalDir, directory.replace("\\", os.path.sep))

    print(f"👀 {bcolors.OKCYAN}Coparando NameSpace para recuperar el path {bcolors.ENDC}")

    # si no existe la carpeta la creamos
    if (not os.path.isdir(finalDir)) and createDirs:
        print(f"{bcolors.OKBLUE}Creamos la carpeta {finalDir} {bcolors.ENDC}")
        os.mkdir(finalDir)
    elif not os.path.isdir(finalDir):
        printError("No existe la carpeta.\n\t  Prueba con la opción -d para crear el directorio", False)



    phpFilePath = os.path.join(finalDir, className + ".php")

    print(f"📝 {bcolors.OKCYAN}Creando ruta para el archivo {bcolors.ENDC}")

    if os.path.exists(phpFilePath) and os.path.isfile(phpFilePath):
        printError(f"Ya existe el archivo {phpFilePath}", False)

    phpFile = open(phpFilePath, "w+")
    phpFile.writelines(("<?php\n\n\n", f"namespace {nameSpace};\n\n", f"\nclass {className}", "{\n\t// content\n}" ))
    phpFile.close()

    print(f"✔️  {bcolors.OKGREEN}{bcolors.BOLD}Archivo creado {bcolors.ENDC}\n")
except:
    pass
