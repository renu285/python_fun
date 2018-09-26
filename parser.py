import os
import sys



class DataParser(object):


    def fillValues(self,lines):
        for line in lines:
            vals = line.split('\t')
            amount = float(vals[6].replace(',','.')) 
            rawsource = vals[7]
            rawsource = " ".join(rawsource.split())
            if(rawsource.split(' ')[0]== 'BEA'):
                amount *= -1
                self.amountTotal += amount
                print amount, rawsource.split(' ')[3]
            else :
                print amount, rawsource
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
