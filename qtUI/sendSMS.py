from twilio.rest import Client

import datetime

def sendSMS():
# we import the Twilio client from the dependency we just installed

    now = datetime.datetime.now()
    currtime = now.strftime("%H:%M")
    messageBody = "Fall Detected at " + currtime

    print(messageBody)


    #Twilio Account SID, Auth Token & phone #s hard-coded from Grace Beal's account
    client = Client("AC25b8ce509ca4b90002ce4d39e083c527", "89077cfe6ae10b47f34750399479914e")

    message = client.messages.create(to="+13012044053",
                           from_="+15025470479",
                           body=messageBody)
    print(message.sid)
