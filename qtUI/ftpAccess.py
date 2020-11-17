import ftplib
import os

def uploadFileToServer(ftp, fileToSend, fileDestDir, fileDestName):
    ftp.cwd(fileDestDir)
    ext = os.path.splitext(fileToSend)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + fileToSend, open(fileToSend, "rb"))
    else:
        ftp.storbinary("STOR " + fileToSend, open(fileToSend, "rb"), 1024)
    print("Written file")


def downloadFileFromServer(ftp, fileToReceive, fileToReceiveDir, fileDestName):
    ftp.cwd(fileToReceiveDir)
    try:
        ftp.retrlines(fileDestName , open(fileToReceive, 'w').write)
    except:
        print("Error")
    print("File recieved")
