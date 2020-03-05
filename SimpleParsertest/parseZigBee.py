import os
import sys
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py





data = rdpcap(sys.argv[1])
num_packets = len(data)
network_key="0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"

print("Numbr of packets : %d "%(num_packets))

num = 1;
for packet in data:
    print("#############################################################################")
    print("packet : %d " %(num)) 
    print(packet.layers)
    print("------------------------------------------------------------")
   

    if(packet.haslayer(ZigbeeNWK)):

        src_addr = packet.getlayer(ZigbeeNWK).fields['source']
        dest_addr = packet.getlayer(ZigbeeNWK).fields['destination']

        print(" Source : 0x%x " %(src_addr))
        print(" Destination : 0x%x " %(dest_addr))


    if(packet.haslayer(ZigbeeSecurityHeader)):
        print(" Need to Decrypt this packet ")
        ed = kbdecrypt(packet,network_key.decode('hex'),verbose=0)
        print (repr(ed))
        if (ed.haslayer(ZigbeeNWKCommandPayload)):
            cmd_id = ed.getlayer(ZigbeeNWKCommandPayload).fields['cmd_identifier']
            if( cmd_id == 8):
                print("  This is a Link status message")
                num_neighbors = ed.getlayer(ZigbeeNWKCommandPayload).fields['entry_count']
                table = ed.getlayer(ZigbeeNWKCommandPayload).fields['link_status_list']
                print(" Number of Neighbors : %d " %(num_neighbors))
                print(" Neighbors : " )
                for i in range(num_neighbors):
                    short_addr = table[0].neighbor_network_address
                    print("          0x%x" %(short_addr))


            else:
                print(ed.getlayer(ZigbeeNWKCommandPayload).fields)

        #if (ed.haslayer(ZigbeeAppDataPayload)):
            #print(" Fields in ZigbeeAppDataPayload")
            #print(ed.getlayer(ZigbeeAppDataPayload).fields)
            #print("Source EP  %d" %(ed.getlayer(ZigbeeAppDataPayload).fields['src_endpoint']))
            #print("Destination EP  %d" %(ed.getlayer(ZigbeeAppDataPayload).fields['dst_endpoint']))
        if(ed.haslayer(ZigbeeClusterLibrary)):

            print("  This a ZCL Message ")
            print(ed.getlayer(ZigbeeClusterLibrary).fields)





    print("------------------------------------------------------------")
    num = num + 1

