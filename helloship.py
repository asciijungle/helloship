#!/usr/bin/python
import itertools
import re
import numpy as np
from subprocess import call
from video import VideoCapture
from gif import GifGenerator
from multiprocessing import Process
from streamloader import StreamLoader
#from shipimage import ImageFetcher
#from twitter_streaming import twitterpush

class HelloShip():

    def __init__(self):
        sl = StreamLoader()
        self.stream = sl.getStream()
        self.knownShips = {}
        pass

    def processEvents(self):
        for event in self.stream:
            userid = event['userid']
            #imagefetcher = ImageFetcher()
            if event['msgid'] == 5:
                # clean name:
                event['name'] = self.cleanName(event['name'])
                # get url
                url = self.getVTUrl(event)
                event['url'] = url
                #print(url)
                #imagefetcher.getImage(url, userid)
            
            if userid not in self.knownShips.keys():
                self.knownShips[userid] =  {event['msgid']: event}
            else:
                self.knownShips[userid].update({event['msgid']: event})

            if 1 in self.knownShips[userid] and 5 in self.knownShips[userid] and self.isnear(userid):
                yield self.knownShips[userid]

    def postProcess(self, ship, fileName):
        gg = GifGenerator()
        gg.generateGif(fileName)
        print "done postprocessing"
    
    def isnear(self, userid):
        radius = 0.02
        event1 = self.knownShips[userid][1]
        event5 = self.knownShips[userid][5]
        if event1['msgid'] == 1:
            distance = np.sqrt((9.948 - event1['pos'][0])**2 + 4*(53.542 - event1['pos'][1])**2)
        if distance <= radius:
            is_near = True
        else:
            is_near = False
        return is_near

    def cleanName(self, name):
        if '@' in name:
            name = re.sub('@+', '', name)
        return name

    def getVTUrl(self,event):
        if event['imo'] is not 0:
            image_url = str('http://www.vesseltracker.com/en/Ships/'+ str(event['imo']) +'.html')
        if event['imo'] is 0:
            image_url = 'no image url'
        return image_url

# main business logic
app = HelloShip()
for closeShip in itertools.ifilter(lambda ship: ship[1]["sog"] > -1, app.processEvents()):
    print ""
    print("Fond close ship. name: {0}  uid: {1}".format(closeShip[5]['name'],closeShip[5]['userid']))
    vc = VideoCapture()
    fileName = vc.captureVideo(closeShip[1]['userid'])
    if fileName is not None:
        p = Process(target=app.postProcess, args=(closeShip, fileName))
        p.start()
