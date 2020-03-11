import os
import sys
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py
from BeeGrapher import *




data = rdpcap(sys.argv[1])
PANID = 4982
network_key = "0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"


BeeParser = BeeGrapher(PANID,network_key)

index = int(sys.argv[2])
for packet in data:
    BeeParser.ParsePacket(packet)
BeeParser.PrintNetworkInfo()
#BeeParser.ParsePacket(data[index])
