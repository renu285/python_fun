import os
import sys



class DataParser(object):

    self.source = []
    self.amount = []
    self.expense = []

    def fillValues(self,lines):
        for line in lines:
            vals = line.split('\t')
            #print vals[6] , vals[7]
            print vals[7].split(' ')[0]


    def __init__(self,dataFile):
        self.lines = [] 
        fp = open(dataFile,'r')
        self.lines = fp.readlines()
        self.fillValues(self.lines)

    def displayRawData(self):
        for line in self.lines:
            print line






def run():
    dp = DataParser(sys.argv[1])


run()
