# encrypted-file-transfer
TCP socket based encrypted file transfer using key,nonce created on file name on extension based folders 

## How it works
It checks the current root directory in which the program is running for all the extension based folders.It then creates a key and nonce based on the file name and encrypts the file using AES-256-EAX. It then sends the encrypted file to the server and the server decrypts the file and saves it in the different directory as the client.