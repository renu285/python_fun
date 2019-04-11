
import urllib2

# OFF
current_state = False 


url_v1="http://blynk-cloud.com/XXXXX/get/v1"

def RawListToData(rawList):

    final_List = []
    chunks = rawList.split(",")

    for chunk in chunks:
        #print chunk
        element = ReturnData(chunk)
        final_List.append(element)

    return final_List

def ReturnData(raw):
    #print len(raw)
    #print raw
    start_index = raw.index('"')
    #print start_index
    end_index = raw.index('"',(start_index + 1),(len(raw)))
    #print end_index
    val = (raw[(start_index + 1) : end_index])
    return int(val)


while 1:
    r_on=urllib2.urlopen(url_ON).read()
    r_joystick=urllib2.urlopen(url_v1).read()
    #r_v2=urllib2.urlopen(url_v2).read()

    stick = RawListToData(r_joystick)
    #on = ReturnData(r_on)
    #v1 = ReturnData(r_v1)
    #v2 = ReturnData(r_v2)
   
    lrCtrl = stick[1]
    frCtrl = stick[0]

    #print (lrCtrl,frCtrl)
    if(frCtrl <= 10):
        print("Forward")
    if(frCtrl >= 1000):
        print("Reverse")
  
    if(lrCtrl <= 10):
        print("Left")
    if(lrCtrl >= 1000):
        print("Right")
