import os
import socket
import glob
import platform
import hashlib
import time

from colorama import just_fix_windows_console
from Crypto.Cipher import AES

from util import *;

# ext_name is a dictionary which contains the extension name as key and the folder name as value
ext_name = {
    "txt": "text",
    "mp4": "video",
    "mp3": "audio"
}

# glob_paths is a list which contains the glob paths of the folders
glob_paths = []

# precond is a function which checks for the preconditions
def precond():
    warnings = [] # warnings is a list which contains the warnings

    if platform.system() == "Windows":
        warnings.append(
            "Windows OS identified, color texts may not work correctly")
        just_fix_windows_console()

    for key in ext_name.keys():
        value = ext_name.get(key)
        if value != None:
            if not os.path.exists(os.path.join(".", value)):
                warnings.append("{0}(.{1}) folder is not present in current directory".format(
                   value, key)) 
                # if the folder is not present in the current directory
                # add into the warnings list 
            else:
                # exists 
                glob_paths.append(confilepath(key,ext_name))

    printwarnings(warnings=warnings)

sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # create a socket object
sender.connect(("localhost",3000)) # bind to free port available

def describeport():
    # describeport is a function which describes the port to which the sender is binded
    print("sender binded to {0}".format(sender.getsockname()))

def sendfile(filepath):
    with open(filepath,"rb") as fhandle:
        filename = os.path.basename(filepath)
        print("sending {0}".format(filename))

        namkey = hashlib.sha256("{0}name".format(filename).encode("utf-8")).digest()[:16] # 16 bytes name key
        namonce = hashlib.sha256("{0}once".format(filename).encode("utf-8")).digest()[:16] # 16 bytes name nonce

        ciper = AES.new(key=namkey,mode=AES.MODE_EAX,nonce=namonce) # create a AES cipher object

        filecontent = fhandle.read() # read the file content
        encrypted = ciper.encrypt(filecontent) # encrypt the file content

        sender.send(filename.encode("utf-8")) # send the filename
        sender.send(str(os.path.getsize(filename=filepath)).encode("utf-8")) # send the filesize
        sender.sendall(encrypted) # send the file content
        sender.send(b"<End>") # send the end of file
        print("send {0}".format(filename)) # print the filename


def handleglob(pathname):
    """
    handleglob is a function which handles the glob path

    Parameters
    ----------
    pathname : str
        the glob path
    """

    gfiles = glob.glob(pathname=pathname) # get the glob files
    warnings = [] # warnings is a list which contains the warnings
    printinfo("handling %s"%(pathname)) # print the info

    if len(gfiles) == 0:
        warnings.append("{0} contains no files".format(os.path.dirname(pathname)))

    for file in gfiles:
        with open(file=file,mode="rb") as fh:
            file_size = os.path.getsize(filename=fh.name)
            if file_size == 0:
                warnings.append("{0} is empty, so it is not send".format(fh.name)) 
            else:
                sendfile(filepath=fh.name) # send the file
    
    printwarnings(warnings=warnings)

precond()
describeport() # describe about the automatically attached port
for gpath in glob_paths:
    handleglob(gpath)
    sender.send(b"<AllEnd>")

time.sleep(5)
sender.close()