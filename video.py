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

        avi_files = {os.path.splitext(f)[0].split("-")[0]: os.path.splitext(f)[0].split("-")[1] for f in os.listdir(direc) if os.path.splitext(f)[1] == ext}
        print avi_files
        
        currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        print("capturing {0}-{1}.avi".format(userid,currentTime))
        return call(["mencoder", "tv://", "-tv", "driver=v4l2:width=640:height=480:device=/dev/video1", "-nosound", "-ovc", "lavc", "-o", str(userid)+"-"+str(currentTime)+".avi", "-endpos", "00:00:05"])
