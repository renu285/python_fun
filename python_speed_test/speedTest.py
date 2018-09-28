import datetime
import os
import sys
import pyspeedtest



class MonitorSpeed(object):

    downloadSpeed = 0.0
    time = " "
    def getSpeed(self):
        st = pyspeedtest.SpeedTest()
        speedSum = 0
        numSamples = 5
        count = 0;

        while(count < 5):
            speedSum += st.download()
            count += 1
        speed = speedSum/numSamples
        speed = speed/1000000
        self.downloadSpeed = speed

    def getTime(self):
        self.time = datetime.datetime.now().strftime("%I:%M%p,%B %d %Y")

    def printTimeSpeed(self):
        self.getSpeed()
        self.getTime()
        print "%.2f,%s" %(self.downloadSpeed,self.time)




monitor = MonitorSpeed()
monitor.printTimeSpeed()
