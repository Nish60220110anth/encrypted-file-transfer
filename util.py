from colorama import Style, Fore, Back
import os

END_OF_TRANSMISSION = "\u0004"
CANCEL = "\u0012"

def createfolder(foldername):
    try:
        os.mkdir(path=os.path.join(".",foldername),mode=0o666)
    except FileExistsError:
        print("file already exists")

def confilepath(file_ext,ext_name):
    return os.path.join(".", ext_name[file_ext], "*.{0}".format(file_ext))

def printwithcolor(frcolor, bgcolor, message):
    print("{0}{1}{2}".format(frcolor, bgcolor, message),end="")
    print(Style.RESET_ALL,end="\n")


def printwarnings(warnings):
    for message in warnings:
        printwithcolor(frcolor=Fore.YELLOW,
                       bgcolor=Back.BLACK, message=message)

def printinfo(message):
    printwithcolor(frcolor=Fore.WHITE,bgcolor=Back.BLUE,message=message)