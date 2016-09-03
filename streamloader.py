#!/usr/bin/python
import socket
import json

class StreamLoader():

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
            result = json.loads(line)
            if result.msgid == 5:
                print result

app = StreamLoader()
app.printStream()

