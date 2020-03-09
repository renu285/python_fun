import os
import sys
import networkx as nx
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py



def updateFileds(ed,raw):
    
    if (ed.haslayer(ZigbeeAppDataPayload)):
        ed.getlayer(ZigbeeAppDataPayload).fields['frame_control'] = int(raw[0:2],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['dst_endpoint'] = int(raw[2:4],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['cluster'] = int(raw[6:8] + raw[4:6],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['profile'] = int(raw[10:12] + raw[8:10],16)
        ed.getlayer(ZigbeeAppDataPayload).fields['src_endpoint'] = int(raw[12:14], 16)






class BeeGrapher(self):


    def __init__(panID,networkKey):

        self.numPackets = 0;
        self.panID = panID
        self.nwKey = networkKey
        self.nodeList = []
        self.networkDict = {}
   



    def Got_LinkStatus_Message(srcAddr, pkt):

        num_neighbors = int(pkt[3],16)
        nodeDict = self.networkDict[srcAddr]
        neigbor_list = nodeDict['NeighborList']
        print(" Number of Neighbors : %d " %(num_neighbors))
        print(" Neighbors : " )
        index = 4 ;
        for i in range(num_neighbors):
            addr = int( pkt[(index + 2) : index + 4] + pkt[index : index+2] ,16)
            print("          0x%x" %(addr))
            if ( addr not in neigbor_list):
                neigbor_list.append(addr)
            #cost = int( (pkt[(index + 6)] + pkt[index + 4]) ,16)
            index = index + 6
        nodeDict['NeighborList'] = neigbor_list

   


    def ParsePacket(self,packet):

        if packet.haslayer(Dot15d4Data):
            panid = packet.getlayer(Dot15d4Data).fields['dest_panid']

        if (panid != self.panID):
            print(" Drop this packet panid [%x] " %(panid))
            self.numPackets = self.numPackets + 1
            return
        
        if(packet.haslayer(ZigbeeNWK)):

        src_addr = packet.getlayer(ZigbeeNWK).fields['source']
        dest_addr = packet.getlayer(ZigbeeNWK).fields['destination']

        if (src_addr not in self.nodeList):
            self.nodeList.append(src_addr)

            NodeDict = { 'NeighborList' : [],
                         'color_x' : 0.0,
                         'color_y' : 0.0,
                         'OnOff'   : 1
                        }

            self.networkDict[src_addr] = NodeDict
            print("Adding  Source : 0x%x to the list " %(src_addr))
            
        if(packet.haslayer(ZigbeeSecurityHeader)):
            
            print(" Need to Decrypt this packet ")
            ed,raw = kbdecrypt(packet,network_key.decode('hex'),verbose=5)
            
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
                    Got_LinkStatus_Message(src_addr, raw)

