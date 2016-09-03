#!/usr/bin/python
import socket
import json
import numpy as np

class StreamLoader():
    def __init__(self):
	self.stream = self.printStream()
	pass

    def printStream(self):
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
            yield json.loads(line)

    def processEvents(self):
	print self.stream
	for event in self.stream:
	    #print(event)
	    if event['msgid'] == 5:
                print(event['name'], event['userid'], event['imo'])
		image_url = ['http://www.vesseltracker.com/en/Ships/'+ str(event['imo']) +'.html']
		print image_url
	#	print(result['userid'], result['pos'])
	#	print result.keys() 

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



app = StreamLoader()
#app.processEvents(app.printStream())
app.processEvents()
#app.isnear()



