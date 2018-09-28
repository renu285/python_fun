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
                dateTime=rawsource.split(" ")[2]
                date=dateTime.split("/")[0]
                time=dateTime.split("/")[1]
                rawsource = rawsource.split("/")[1]
                source = rawsource.split(",")[0]
                source = source.split(None,1)[1]
                source = ' '.join(source.split()[:2])
                amount *= -1
                self.amountTotal += amount
                print "%4.2f\t%6s\t%6s\t%s" %(amount, date,time, source)
            else :
                try:
                    name_index = rawsource.index("NAME")
                    dateTime=rawsource.split("/")[12]
                    rawsource = rawsource[name_index:]
                    source = rawsource.split("/")[1]
                    if(amount < 0) :
                        amount *= -1
                        self.amountTotal += amount
                    try:
                        date = dateTime.split(" ")[0]
                        time = dateTime.split(" ")[1]
                    except IndexError:
                        date = " "
                        time = " " 
                    print "%4.2f\t%6s\t%6s\t%s" %(amount,date,time, source)

                except ValueError:
                    try:
                        name_index = rawsource.index("Naam")
                        rawsource = rawsource[name_index:]
                        source = rawsource.split(":")[1]
                        if(amount < 0) :
                            amount *= -1
                            self.amountTotal += amount
                            print "%4.2f\t%6s\t%6s\t%s" %(amount, '    ','     ', source)
                    except ValueError:
                        if(amount < 0) :
                            amount *= -1
                            self.amountTotal += amount
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
