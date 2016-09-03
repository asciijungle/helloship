#!/usr/bin/python
import socket
import json
import numpy as np
import sys
from printf import printf
from colors import bcolors

class StreamLoader():
    def __init__(self):
        self.stream = self.getStream()
        self.knownShips = {}
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

    def saveEvents(self):
	with open('streamdata.json', 'a+') as f:
    	     json.dump(event, f)

    def isnear(self):
	print self.stream
	radius = 0.0128
	for event in self.stream:
	    if event['msgid'] == 1:
		distance = np.sqrt((9.95 - event['pos'][0])**2 + (53.544 - event['pos'][1])**2)
		if distance <= radius:
			is_near = True
			print('this ship is near: ', event['userid']) 
		else:
			is_near = False

    def processEvents(self):
        for event in self.stream:

            userid = event['userid']

            if event['msgid'] == 5:
                url = self.getVTUrl(event)
                event['url'] = url
            
            if userid not in self.knownShips.keys():
                self.knownShips[userid] =  {event['msgid']: event}
            else:
                self.knownShips[userid].update({event['msgid']: event})

            if 1 in self.knownShips[userid] and 5 in self.knownShips[userid]:
               yield self.knownShips[userid]


            #completeShip = self.checkForCompleteData(userid)
            #if completeShip is not None:
            #    print completeShip

    def getVTUrl(self,event):
        if event['imo'] is not 0:
            image_url = ['http://www.vesseltracker.com/en/Ships/'+ str(event['imo']) +'.html']
	    return image_url
        else:
            return None

    def printEventID(self,event):
        msgid = str(event['msgid'])
        color = None
        if msgid is "1":
            color = bcolors.HEADER
        if msgid is "5":
            color = bcolors.OKGREEN
        if msgid is "3":
            color = bcolors.OKBLUE
        printf(color+str(msgid)+bcolors.ENDC)


    #def checkForCompleteData(self,userid):


app = StreamLoader()
for closeShip in app.processEvents():
    print "==================="
    print "FOUND CLOSE SHIP!!!"
    print "==================="
    print closeShip
    print "==================="
    print ""

