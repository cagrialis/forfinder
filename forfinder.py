import os
import sys
import time
import zipfile
import threading
from datetime import datetime
import colorama

from colorLib import bcolors as bc
from colorama import *

NOW = datetime.utcnow().replace(microsecond=0)

def writeName():

    name = f"""\
{Fore.CYAN}
   ▄████████  ▄██████▄     ▄████████         ▄████████  ▄█  ███▄▄▄▄   ████████▄     ▄████████    ▄████████ 
  ███    ███ ███    ███   ███    ███        ███    ███ ███  ███▀▀▀██▄ ███   ▀███   ███    ███   ███    ███ 
  ███    █▀  ███    ███   ███    ███        ███    █▀  ███▌ ███   ███ ███    ███   ███    █▀    ███    ███ 
 ▄███▄▄▄     ███    ███  ▄███▄▄▄▄██▀       ▄███▄▄▄     ███▌ ███   ███ ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███▀▀▀     ███    ███ ▀▀███▀▀▀▀▀        ▀▀███▀▀▀     ███▌ ███   ███ ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███        ███    ███ ▀███████████        ███        ███  ███   ███ ███    ███   ███    █▄  ▀███████████ 
  ███        ███    ███   ███    ███        ███        ███  ███   ███ ███   ▄███   ███    ███   ███    ███ 
  ███         ▀██████▀    ███    ███        ███        █▀    ▀█   █▀  ████████▀    ██████████   ███    ███ 
                          ███    ███                                                            ███    ███             
							    	{Style.RESET_ALL}v.1.0 https://github.com/cagrialis/forfinder
    """

    print(name)

def typeScan(rootDirectory):
    jarExt = [".jar", ".war", ".ear", ".zip", ".aar"]
    for entry in os.scandir(rootDirectory):
        if entry.is_dir():
            pathFile = f"{rootDirectory}{os.sep}{entry.name}"
            with open('folders.txt', 'a') as f:
                f.write(repr(pathFile) + '\n')
            typeScan(pathFile)
        else:
            fileType = os.path.splitext(entry.name)[-1]
            pathFile = f"{rootDirectory}{os.sep}{entry.name}"
            if fileType in jarExt:
                try:
                    readOtherType(pathFile)
                except:
                    error = f"{Style.BRIGHT}[{NOW}]{Fore.RED}[ERROR-BAD FILE] => {Fore.BLUE}[FILE]: {Fore.YELLOW}{pathFile}{Style.RESET_ALL}"
                    writeErrorFile(pathFile)
                    checkString = f"{Style.BRIGHT}[CHECK MANUEL]{Style.RESET_ALL}"
                    print(error, checkString)
            else:
                readLines(pathFile)

def readLines(file):
    with open(file, 'rb') as f:
        for line in f.readlines():
            a = str(line).find(sys.argv[2])
            if a != -1:
               result = f"{Style.BRIGHT}[{NOW}]{Fore.GREEN}[SUCCESS-FILE FOUND] => {Fore.BLUE}[FILE]: {Fore.BLUE}{file}{Style.RESET_ALL}"
               writeFile(file+"\n")
               print(result)

def readOtherType(otherFile):
    with zipfile.ZipFile(otherFile, 'r') as zip:
        nameList = zip.namelist()
        for name in nameList:
            lastName = zip.read(name=name)
            fileControl = (str(lastName)).find(sys.argv[2])
            if fileControl != -1:
                result = f"{Style.BRIGHT}[{NOW}]{Fore.GREEN}[SUCCESS-FILE FOUND] => {Fore.BLUE}[FILE]: {Fore.BLUE}{otherFile}\{str(name)}{Style.RESET_ALL}"
                writeFile(otherFile+"\\"+str(name)+"\n")
                print(result)

def writeFile(filePath):
    with open('file.txt', 'a') as f:
        f.write(filePath + "\n")

def writeErrorFile(errorPath):
    with open('error.txt', 'a') as f:
        f.write(errorPath + "\n")

def startProg():
    colorama.init()
    th1 = threading.Thread(target=writeName())
    th1.start()
    print(f"{Style.BRIGHT}[{NOW}]Searching files at {Fore.MAGENTA}\"{sys.argv[1]}\"...{Style.RESET_ALL}\n")
    time.sleep(10)
    th2 = threading.Thread(target=typeScan(sys.argv[1]))
    th2.start()
    print(f"\n{Style.BRIGHT}[{NOW}]{Fore.CYAN}[Scanned Folders: \"folders.txt\"]{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}[{NOW}]{Fore.YELLOW}[Search Results: \"files.txt\"]{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}[{NOW}]{Fore.RED}[Error Messages: \"error.txt\"]{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        startProg()
    except KeyboardInterrupt:
        print("\nExiting...")
