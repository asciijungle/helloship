from subprocess import call
import os
import glob
import shutil

class GifGenerator():
    def __init__(self):
        pass

    def generateGif(self, fileName):
        print ("generating gif of {0}".format(fileName))
        tempPath = "./frames-"+fileName
        if not os.path.exists(tempPath):
            os.makedirs(tempPath)
        call(["ffmpeg", "-ss", "1", "-i", fileName + ".avi", "-r", "5", tempPath + "/frame-%03d.jpg"])
        call(["convert", "-delay", "5", "-loop", "0", "-layers", "Optimize", "-fuzz", "3%", tempPath + "/*.jpg", fileName + ".gif"])
        shutil.rmtree(tempPath, ignore_errors=True)
        return fileName + ".gif"
