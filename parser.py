import os
import sys



class DataParser(object):


    def fillValues(self,lines):
        for line in lines:
            vals = line.split('\t')
            amount = float(vals[6].replace(',','.')) * -1
            rawsource = vals[7]
            rawsource = " ".join(rawsource.split())
            if(rawsource.split(' ')[0]== 'BEA'):
                self.amountTotal += amount
                print amount, rawsource.split(' ')[3]
        print "Total Amount spent : ", self.amountTotal 

    def __init__(self,dataFile):
        self.source = []
        self.amountTotal = 0.0 
        self.expense = []
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
