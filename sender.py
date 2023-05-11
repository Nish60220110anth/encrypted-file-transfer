import os
import socket
import glob
import platform
import hashlib
import time

from colorama import just_fix_windows_console
from Crypto.Cipher import AES

from util import *;


key = b"TheNeuralNineKey"
nonce = b"TheNeuralNineNce"

ext_name = {
    "txt": "text",
    "mp4": "video",
    "mp3": "audio"
}

glob_paths = []

def precond():
    warnings = []

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
            else:
                # exists 
                glob_paths.append(confilepath(key,ext_name))

    printwarnings(warnings=warnings)

sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sender.connect(("localhost",3000)) # bind to free port available

def describeport():
    print("sender binded to {0}".format(sender.getsockname()))

def sendfile(filepath):
    with open(filepath,"rb") as fhandle:
        filename = os.path.basename(filepath)
        print("sending {0}".format(filename))
        namkey = hashlib.sha256("{0}name".format(filename).encode("utf-8")).digest()[:16]
        namonce = hashlib.sha256("{0}once".format(filename).encode("utf-8")).digest()[:16]

        ciper = AES.new(key=namkey,mode=AES.MODE_EAX,nonce=namonce)
        filecontent = fhandle.read()
        encrypted = ciper.encrypt(filecontent)

        sender.send(filename.encode("utf-8"))
        sender.send(str(os.path.getsize(filename=filepath)).encode("utf-8"))
        sender.sendall(encrypted)
        sender.send(b"<End>")
        print("send {0}".format(filename))


def handleglob(pathname):
    gfiles = glob.glob(pathname=pathname)
    warnings = []
    printinfo("handling %s"%(pathname))

    if len(gfiles) == 0:
        warnings.append("{0} contains no files".format(os.path.dirname(pathname)))

    for file in gfiles:
        with open(file=file,mode="rb") as fh:
            file_size = os.path.getsize(filename=fh.name)
            if file_size == 0:
                warnings.append("{0} is empty, so it is not send".format(fh.name)) 
            else:
                sendfile(filepath=fh.name)
    
    printwarnings(warnings=warnings)

precond()
describeport() # describe about the automatically attached port
for gpath in glob_paths:
    handleglob(gpath)
    sender.send(b"<AllEnd>")

time.sleep(5)
sender.close()