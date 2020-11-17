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
    lf = open(fileToReceive, "wb")
    try:
        ftp.retrbinary("RETR " + fileDestName, lf.write, 8*1024)
        print("File recieved")
        lf.close()
    except:
        print("File not found")

def deleteFileFromServer(ftp, fileToDelete, fileToDeleteDir):
    ftp.cwd(fileToDeleteDir)
    try:
        ftp.delete(fileToDelete)
        print("File deleted")
    except:
        print("File not found")
