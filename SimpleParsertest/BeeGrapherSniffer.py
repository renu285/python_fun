import os
import sys
import subprocess
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py
from BeeGrapher import *
from time import sleep



#data = rdpcap(sys.argv[1])
PANID = 0x215e 
network_key = "0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"
fig, ax = plt.subplots(figsize=(10,10))
BeeParser = BeeGrapher(PANID,network_key)

class Grapher():


    def __init__(self):
        self.G = nx.Graph()
   
    def AddNode(self,node):
        self.G.add_node(node)

    def AddEdge(self,node1,node2):
        self.G.add_edge(node1,node2)


def pkt_callback(pkt):
    #pkt.show() # debug statement
    BeeParser.ParsePacket(pkt)


def LinkStatusCallback(srcAddr):
    
    nodeDict = BeeParser.networkDict[srcAddr]
    neigbor_list = nodeDict['NeighborList']
    for node in neigbor_list:
        graph.AddEdge(srcAddr, node)

def NewNodeCallback(srcAddr):
    graph.AddNode(srcAddr)



def update(num):

    ax.clear()
    #nx.draw_shell(graph.G)
    #nx.draw_shell(graph.G, node_color = BeeParser.ColorMap)
    pos  = nx.shell_layout(graph.G)
    nx.draw_networkx_nodes(graph.G, pos=pos, nodelist = set(graph.G.nodes()), node_color = BeeParser.ColorMap )
    nx.draw_networkx_edges(graph.G, pos=pos)
    #null_nodes.set_edgecolor("blue")
    plt.axis('off')



def SnifferThread(data):
    
    sniff(offline=sys.argv[1], prn=pkt_callback, store=0)


BeeParser.NewNodeCallback = NewNodeCallback
BeeParser.LinkStatusCallback = LinkStatusCallback
graph = Grapher()
ani = animation.FuncAnimation(fig, update, frames=1, interval=500, repeat=True)





t = threading.Thread(target=SnifferThread, args=("blah",))
t.start()

plt.show()
