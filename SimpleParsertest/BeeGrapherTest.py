import os
import sys
from scapy.all import *
from killerbee import *
from killerbee.scapy_extensions import *    # this is explicit because I didn't want to modify __init__.py
from BeeGrapher import *
from time import sleep



data = rdpcap(sys.argv[1])
PANID = 4982
network_key = "0BAD0BAD0BAD0BAD0BAD0BAD0BAD0BAD"
fig, ax = plt.subplots(figsize=(10,10))
G = nx.Graph()
BeeParser = BeeGrapher(PANID,network_key)




def ParserThread(data):
    for packet in data:
        BeeParser.ParsePacket(packet)
        sleep(0)


def LinkStatusCallback(srcAddr):
    
    nodeDict = BeeParser.networkDict[srcAddr]
    neigbor_list = nodeDict['NeighborList']
    for node in neigbor_list:
        G.add_edge(srcAddr,node)

def NewNodeCallback(srcAddr):
    G.add_node(srcAddr)



def update(num):

    ax.clear()
    nx.draw_shell(G)
    #null_nodes = nx.draw_networkx_nodes(G, pos=pos)
    #nx.draw_networkx_edges(G, pos, width=0.25, alpha=0.5)
    #null_nodes.set_edgecolor("blue")
    plt.axis('off')


BeeParser.NewNodeCallback = NewNodeCallback
BeeParser.LinkStatusCallback = LinkStatusCallback
ani = animation.FuncAnimation(fig, update, frames=1, interval=500, repeat=True)


x = threading.Thread(target=ParserThread, args=(data,))
x.start()

plt.show()
#BeeParser.PrintNetworkInfo()
#BeeParser.ParsePacket(data[index])
