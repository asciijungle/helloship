from subprocess import call
import os
import datetime

class VideoCapture():
    def __init__(self):
        pass

    def captureVideo(self, userid):
        direc = os.getcwd()
        ext = ".avi"
        file_dict = {}

        timestamps = {int(os.path.splitext(f)[0].split("-")[0]): int(os.path.splitext(f)[0].split("-")[1]) for f in os.listdir(direc) if os.path.splitext(f)[1] == ext}
        currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        if(userid in timestamps.keys()):
            timeout = timestamps[userid] + 500
            if((timestamps[userid] + 500) <= int(currentTime)):
                print("capturing {0}-{1}.avi".format(userid,currentTime))
                return self.recordVideo(userid,currentTime)
            else:
                print "not capturing video. timestamp: {0} current time: {1}".format(timestamps[userid],currentTime)
        else:
            print("no video for userid: {0}. thus capturing video".format(userid))
            return self.recordVideo(userid,currentTime)

    def recordVideo(self,userid,timestamp):
        return call(["mencoder", "tv://", "-tv", "driver=v4l2:width=640:height=480:device=/dev/video1", "-nosound", "-ovc", "lavc", "-o", str(userid)+"-"+str(timestamp)+".avi", "-endpos", "00:00:05"])
