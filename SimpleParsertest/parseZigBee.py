import os
import sys
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py





data = rdpcap(sys.argv[1])
PANID = 4982
num_packets = len(data)
network_key = "0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"



NodeList = []

NetworkDict = {}


print("Numbr of packets : %d "%(num_packets))



def Got_LinkStatus_Message(srcAddr, pkt):

    print(pkt)
    #num_neighbors = pkt.getlayer(ZigbeeNWKCommandPayload).fields['entry_count']
    num_neighbors = int(pkt[3],16) 
    nodeDict = NetworkDict[srcAddr]
    neigbor_list = nodeDict['NeighborList']
    print(" Number of Neighbors : %d " %(num_neighbors))
    print(" Neighbors : " )


    index = 4 ;

    for i in range(num_neighbors):
        addr = int( pkt[(index + 4) : index + 6] + pkt[index : index+2] ,16)
        print("          0x%x" %(addr))
        if ( addr in neigbor_list):
            neigbor_list.append(addr)

        #cost = int( (pkt[(index + 6)] + pkt[index + 4]) ,16)
        index = index + 6


'''
    table = pkt.getlayer(ZigbeeNWKCommandPayload).fields['link_status_list']
    print( pkt.getlayer(ZigbeeNWKCommandPayload).fields)
    neigbor_list = []
    if (srcAddr in NodeList):
        for i in range(num_neighbors):
            short_addr = table[i].neighbor_network_address
            if (short_addr not in neigbor_list):
                neigbor_list.append(short_addr)
            print("          0x%x" %(short_addr))
'''

def Got_ZCL_OnOff_Message(srcAddr,pkt):

    print (" This is OnOff Message ")
    status = int(pkt[20:],16)
    print("     On Off status %d"%(status))
    if (srcAddr in NodeList):
        nodeDict = NetworkDict[srcAddr]
        nodeDict['onOff'] = status






num = 1;
for packet in data:
    print("#############################################################################")
    print("packet : %d " %(num)) 
    #print(packet.layers)
    print("------------------------------------------------------------")
   

    if packet.haslayer(Dot15d4Data):
        panid = packet.getlayer(Dot15d4Data).fields['dest_panid']
        print(panid)

        if (panid != PANID):
            print(" Drop this packet panid %x " %(panid))
            num = num + 1
            continue


    if(packet.haslayer(ZigbeeNWK)):

        src_addr = packet.getlayer(ZigbeeNWK).fields['source']
        dest_addr = packet.getlayer(ZigbeeNWK).fields['destination']

        print(packet.getlayer(ZigbeeNWK).fields)

        #print(" Source : 0x%x " %(src_addr))
        #print(" Destination : 0x%x " %(dest_addr))

        if (src_addr not in NodeList):
            NodeList.append(src_addr)
            NodeDict = { 'NeighborList' : [],
                         'color_x' : 0.0,
                         'color_y' : 0.0,
                         'OnOff'   : 1
                        }
            NetworkDict[src_addr] = NodeDict
            print("Adding  Source : 0x%x " %(src_addr))

    if(packet.haslayer(ZigbeeSecurityHeader)):
        print(" Need to Decrypt this packet ")
        ed,raw = kbdecrypt(packet,network_key.decode('hex'),verbose=5)
        #print (repr(ed))
        #print (type(raw))
        if (ed.haslayer(ZigbeeNWKCommandPayload)):
            cmd_id = ed.getlayer(ZigbeeNWKCommandPayload).fields['cmd_identifier']
            if( cmd_id == 8):
                print("  This is a Link status message")
                Got_LinkStatus_Message(src_addr, raw)
            else:
                print(ed.getlayer(ZigbeeNWKCommandPayload).fields)

        if (ed.haslayer(ZigbeeAppDataPayload)):

            ed.getlayer(ZigbeeAppDataPayload).fields['frame_control'] = int(raw[0:2],16)
            ed.getlayer(ZigbeeAppDataPayload).fields['dst_endpoint'] = int(raw[2:4],16)
            ed.getlayer(ZigbeeAppDataPayload).fields['cluster'] = int(raw[6:8] + raw[4:6],16)
            ed.getlayer(ZigbeeAppDataPayload).fields['profile'] = int(raw[10:12] + raw[8:10],16)
            ed.getlayer(ZigbeeAppDataPayload).fields['src_endpoint'] = int(raw[12:14], 16)

        if(ed.haslayer(ZigbeeClusterLibrary)):

            print("  This a ZCL Message ")

            clusterID = ed.getlayer(ZigbeeAppDataPayload).fields['cluster']
            profileID = ed.getlayer(ZigbeeAppDataPayload).fields['profile'] 

            if (clusterID == 6 and profileID == 260):
                Got_ZCL_OnOff_Message(src_addr, raw)
            


            #print(ed.getlayer(ZigbeeClusterLibrary).fields)




    print("------------------------------------------------------------")
    num = num + 1

print(NodeList)
print(NetworkDict)
