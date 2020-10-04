import os
import sys
import signal
import subprocess
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py
from BeeGrapherV2 import *
from time import sleep
import paho.mqtt.publish as publish
import json


PANID = 0x79eb 
network_key = "0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"
BeeParser = BeeGrapher(PANID,network_key)
host_addr = "192.168.2.59"



def PublishMQTT(topic,payload):
    print("Publishing topic %s  Payload %s " %(topic,payload))
    publish.single(topic, payload, hostname=host_addr)



def pkt_callback(pkt):
    #pkt.show() # debug statement
    BeeParser.ParsePacket(pkt)



def ColorControlCallback(destAddr, color):
    payload = {"Id" : hex(destAddr), "Color": color}
    data_out = json.dumps(payload)
    PublishMQTT("ChangeColor",data_out)

def OnOffStatusCallback(destAddr, color):
    payload = {"Id" : hex(destAddr), "Color": color}
    data_out = json.dumps(payload)
    PublishMQTT("ChangeColor",data_out)



def LinkStatusCallback(srcAddr):
   
    print("Publishing Link status")
    nodeDict = BeeParser.networkDict[srcAddr]
    neighbor_list = nodeDict['NeighborList']
    payload = {"Id" : hex(srcAddr), "Neighbors": neighbor_list}
    data_out = json.dumps(payload)
    PublishMQTT("ReceivedLinkStatus",data_out)

def NewNodeCallback(srcAddr):
    payload = {"Id" : hex(srcAddr), "Color": "#ffee00"}
    data_out = json.dumps(payload)
    PublishMQTT("NewNode",data_out)



def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    t.join() 
    sys.exit(0)


def SnifferThread(data):
    sniff(offline="/tmp/whsniff", prn=pkt_callback, store=0)
    signal.signal(signal.SIGINT, signal_handler)


BeeParser.NewNodeCallback = NewNodeCallback
BeeParser.LinkStatusCallback = LinkStatusCallback
BeeParser.OnOffCallback = OnOffStatusCallback
BeeParser.ColorControlCallback = ColorControlCallback


t = threading.Thread(target=SnifferThread, args=("blah",))
t.start()
signal.signal(signal.SIGINT, signal_handler)

