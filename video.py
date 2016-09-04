from subprocess import call
import os
import glob
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
        filename =  str(userid)+"-"+str(timestamp)
        call(["mencoder", "tv://", "-tv", "driver=v4l2:width=640:height=480:device=/dev/video1", "-nosound", "-ovc", "lavc", "-o", filename+".avi", "-endpos", "00:00:10"])
        self.generateGif(filename)


    def generateGif(self, fileName):
        print ("generating gif of {0}".format(fileName))
        call(["ffmpeg", "-ss", "1", "-i", fileName + ".avi", "-r", "5", "frames/frame-%03d.jpg"])
        call(["convert", "-delay", "5", "-loop", "0", "-layers", "Optimize", "-fuzz", "3%", "frames/*.jpg", fileName + ".gif"])
        files = glob.glob('./frames/*')
        for f in files:
            os.remove(f)
        return fileName + ".gif"
