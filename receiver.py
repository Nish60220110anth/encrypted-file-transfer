import hashlib
import socket
import os

import tqdm
from Crypto.Cipher import AES
from util import createfolder

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.bind(("localhost",3000))
client.listen()

canaccept = True 

def handleclient(conn,addr):
    print("{0} started getting served".format(addr))

    fileDone = False
    allDone = False
    
    while not allDone:
        file_bytes = b""
        filename = conn.recv(1024).decode("utf-8")
        filesize = conn.recv(1024).decode("utf-8")
        print("filename: {0}".format(filename))
        print("filesize: {0}".format(filesize))

        namkey = hashlib.sha256("{0}name".format(filename).encode("utf-8")).digest()[:16]
        namonce = hashlib.sha256("{0}once".format(filename).encode("utf-8")).digest()[:16]

        ciper = AES.new(key=namkey,mode=AES.MODE_EAX,nonce=namonce)
        progress = tqdm.tqdm(unit="B",unit_scale=True,
                        unit_divisor=1000,
                        total=int(filesize))
        while not fileDone:
            data = conn.recv(1024)
            if file_bytes[-5:0] == b"<End>":
                fileDone = True
            if file_bytes[-8:0] == b"<AllEnd>":
                allDone = True
            else:
                file_bytes += data
            
            progress.update(1024)
        
            new_filename = os.path.join(".","server",filename)
            with open(new_filename,"wb") as fh:
                fh.write(ciper.decrypt(file_bytes))

    print("{0} connection ended".format(addr))
    conn.close()

total = 0

def server():
    global canaccept
    global total

    while canaccept:
        print("Waiting for new client!")
        conn , addr = client.accept()
        total += 1
        handleclient(conn=conn,addr=addr)

        if total == 20:
            print("connection closing for all")
            canaccept = False

createfolder("server")
server()