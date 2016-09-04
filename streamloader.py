import sys
import socket
import json
from colors import bcolors
from printf import printf

class StreamLoader():
    def __init__(self):
        pass

    def getStream(self):
        print "running printStream()"
        #create an INET, STREAMing socket
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #now connect to the web server on port 80
        # - the normal http port
        sock.connect(("78.46.149.194", 1895))
        
        infile = sock.makefile()

        while True:
            line = infile.readline()
            if not line: break
            event = json.loads(line)
            self.printEventID(event)
            sys.stdout.flush()
            yield event


    def printEventID(self,event):
        msgid = str(event['msgid'])
        color = bcolors.BOLD
        if msgid is "1":
            color = bcolors.HEADER
        if msgid is "5":
            color = bcolors.OKGREEN
        if msgid is "3":
            color = bcolors.OKBLUE
        printf(color+str(msgid)+bcolors.ENDC)

    def saveEvents(self, event):
        with open('streamdata.json', 'a+') as f:
            json.dump(event, f)

