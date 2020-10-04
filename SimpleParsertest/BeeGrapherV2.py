import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rgbxy import Converter
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py
from time import sleep
import subprocess
from rgbxy import Converter

def updateFileds(ed,raw):
    
    if (ed.haslayer(ZigbeeAppDataPayload)):
        ed.getlayer(ZigbeeAppDataPayload).fields['frame_control'] = int(raw[0:2],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['dst_endpoint'] = int(raw[2:4],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['cluster'] = int(raw[6:8] + raw[4:6],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['profile'] = int(raw[10:12] + raw[8:10],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['src_endpoint'] = int(raw[12:14], 16)



def DefaultCallback():
    return

def GetFloat(num):

    print(num)
    num = int(num)
    num = hex(num)
    command = ['./hexToFloat' , str(num)] 
    pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log_data, dummy = pid.communicate()
    return float(log_data)

def GetCmapValue(x,y):

    #x = str(hex(x))
    #x = x[2:]
    #y = str(hex(y))
    #y = y[2:]
    
    x = GetFloat(x)
    y = GetFloat(y)

    converter = Converter() 
    (r,g,b) = converter.xy_to_rgb(x,y)
    r = str(hex(r))
    r = r[2:]
    g = str(hex(g))
    g = g[2:]
    b = str(hex(b))
    b = b[2:]
    if(len(r) == 1):
        r = "0"+ r 
    if(len(g) == 1):
        g = "0" + g
    if(len(b) == 1):
        b = "0" + b
    value = '#' + r  + g + b 
    return value



class BeeGrapher(object):


    def __init__(self, panID, networkKey):

        self.numPackets = 0;
        self.panID = panID
        self.nwKey = networkKey
        self.nodeCount = 0
        self.nodeList = []
        self.networkDict = {}
        self.NewNodeCallback = DefaultCallback
        self.LinkStatusCallback = DefaultCallback
        self.OnOffCallback = None 
        self.ColorControlCallback = None 
        self.ColorMap = []

    def ParsePacket(self,packet):

        parser = threading.Thread(target=self.ProcessPacket , args=(packet,))
        parser.start()

    def PrintNetworkInfo(self):
        for k,v in self.networkDict.iteritems():
            print("Node : %x " %(k))
            for kn,vn in v.iteritems():
                print kn,vn
        
        print(self.G.nodes())

    def Got_ZCL_OnOff_Message(self,srcAddr, destAddr, pkt):

        zclPyloadLength = len(pkt) - 16

        if (destAddr == 0xfffd):
            print("Ignore group cast for now ")
            return
    
        if(zclPyloadLength > 6):
            print("Probably Read Atrribute or Read Attr Response Ignore for now")
            return

        print (" This is OnOff Message ")
        status = int(pkt[20:],16)
        print (" Status : %d " %( status))
        print("     On Off status %d"%(status))
        if (destAddr in self.nodeList):
            nodeDict = self.networkDict[destAddr]
            nodeDict['OnOff'] = status
            if(status == 0x00):
                nodeId = nodeDict['Id']
                self.ColorMap[nodeId] = '#000000'
                self.OnOffCallback(destAddr,'#000000')
            if(status == 0x01):
                x = nodeDict['color_x'] 
                y = nodeDict['color_y']
                colorValue = GetCmapValue(x,y)
                nodeId = nodeDict['Id']
                self.ColorMap[nodeId] = colorValue
                self.OnOffCallback(destAddr,colorValue)



    def Got_ColorControl_Message(self,srcAddr, destAddr, pkt):

        print(" Color Control Message " )
        zcl_frame_type = int(pkt[16:18], 16)
        #print(zcl_frame_type)
        if (zcl_frame_type != 0x11):
            print("Read attributes and responses Ignored")
            return

        cmd = int(pkt[20:22])

        if(cmd == 0x07):
            x_high = int(pkt[22:24] , 16)
            x_low =  int(pkt[24:26] , 16)
            y_high = int(pkt[26:28] , 16)
            y_low =  int(pkt[28:30] , 16)

            x = x_high |  (x_low << 8)
            y = y_high |  (y_low << 8)

            colorValue = GetCmapValue(x,y)
            nodeDict = self.networkDict[destAddr]
            nodeId = nodeDict['Id']
            nodeDict['color_x'] = x
            nodeDict['color_y'] = y
            print("ColoValue : %s " %(colorValue))
            self.ColorMap[nodeId] = colorValue
            self.ColorControlCallback(destAddr,colorValue)

    
    def Got_LinkStatus_Message(self, srcAddr, pkt):

        triggerCallback = False
        num_neighbors = int(pkt[3],16)
        nodeDict = self.networkDict[srcAddr]
        neigbor_list = nodeDict['NeighborList']
        print(" Number of Neighbors : %d " %(num_neighbors))
        print(" Neighbors : " )
        index = 4 ;
        for i in range(num_neighbors):
            addr = int( pkt[(index + 2) : index + 4] + pkt[index : index+2] ,16)
            print("          0x%x" %(addr))
            if ( hex(addr) not in neigbor_list):
                neigbor_list.append(hex(addr))
                triggerCallback = True
            #cost = int( (pkt[(index + 6)] + pkt[index + 4]) ,16)
            index = index + 6
        nodeDict['NeighborList'] = neigbor_list

        if(triggerCallback):
            self.LinkStatusCallback(srcAddr)



    def ProcessPacket(self,packet):

        panid = 0
        cmd_id = -1
    
        #print("------------------------------------------")
        #print(self.numPackets)
        #print("------------------------------------------")

        if packet.haslayer(Dot15d4Data):
            panid = packet.getlayer(Dot15d4Data).fields['dest_panid']

        if (panid != self.panID):
            #print(" Drop this packet panid [%x] " %(panid))
            self.numPackets = self.numPackets + 1
            return
        
        if(packet.haslayer(ZigbeeNWK)):
            
            src_addr = packet.getlayer(ZigbeeNWK).fields['source']
            dest_addr = packet.getlayer(ZigbeeNWK).fields['destination']

        if (src_addr not in self.nodeList):
            self.nodeList.append(src_addr)
            #self.G.add_node(src_addr)
            NodeDict = { 'NeighborList' : [],
                         'srcAddr': src_addr,
                         'color_x' : 0.4685,
                         'color_y' : 0.4620,
                         'Id'      : self.nodeCount,
                         'OnOff'   : 1
                        }
            self.ColorMap.append('#ffee00')
            self.nodeCount = self.nodeCount + 1 
            self.networkDict[src_addr] = NodeDict
            #print("Adding  Source : 0x%x to the list " %(src_addr))
            self.NewNodeCallback(src_addr)

        if(packet.haslayer(ZigbeeSecurityHeader)):
            
            #print(" Need to Decrypt this packet ")
            ed,raw = kbdecrypt(packet,self.nwKey.decode('hex'),verbose=0)
            
            if (ed.haslayer(ZigbeeNWKCommandPayload)):
                
                cmd_id = ed.getlayer(ZigbeeNWKCommandPayload).fields['cmd_identifier']
            
            if (ed.haslayer(ZigbeeAppDataPayload)):

                ed.getlayer(ZigbeeAppDataPayload).fields['frame_control'] = int(raw[0:2],16)
                ed.getlayer(ZigbeeAppDataPayload).fields['dst_endpoint'] = int(raw[2:4],16)
                ed.getlayer(ZigbeeAppDataPayload).fields['cluster'] = int(raw[6:8] + raw[4:6],16)
                ed.getlayer(ZigbeeAppDataPayload).fields['profile'] = int(raw[10:12] + raw[8:10],16)
                ed.getlayer(ZigbeeAppDataPayload).fields['src_endpoint'] = int(raw[12:14], 16)

                
            if( cmd_id == 8):
                print("  Received a Link status message")
                self.Got_LinkStatus_Message(src_addr, raw)

            if(ed.haslayer(ZigbeeClusterLibrary)):
                    
                clusterID = ed.getlayer(ZigbeeAppDataPayload).fields['cluster']
                profileID = ed.getlayer(ZigbeeAppDataPayload).fields['profile']
                    
                if (clusterID == 6 and profileID == 260):                        

                    self.Got_ZCL_OnOff_Message(src_addr, dest_addr, raw)
                        
                if (clusterID == 0x0300 and profileID == 260):
                    #print(ed.getlayer(ZigbeeAppDataPayload).fields)
                    #print( ed.getlayer(ZigbeeAppDataPayload).fields['frame_control'])
                    self.Got_ColorControl_Message(src_addr, dest_addr, raw)
                        
                if (clusterID == 0x0800 and profileID == 260):
                    #print(" Level control message  Ignore for now")
                    self.numPackets = self.numPackets+1
                    return


'''
data = rdpcap(sys.argv[1])
PANID = 4982
network_key = "0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"


BeeParser = BeeGrapher(PANID,network_key)

index = int(sys.argv[2])
for packet in data:
    BeeParser.ParsePacket(packet)
    sleep(1)

BeeParser.PrintNetworkInfo()
ani = animation.FuncAnimation(BeeParser.fig, BeeParser.update , frames=1, interval=500, repeat=True)
plt.show()
'''
