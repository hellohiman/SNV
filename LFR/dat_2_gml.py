#coding=utf-8
import networkx as nx
from collections import defaultdict

def transfer_2_gml():

    '''--------------------------------------------------------------------------
    function: 将LFR的network.dat和community.dat转化为.gml文件
    parameter:
    return:
    -------------------------------------------------------------------------------'''

    nodes_labels={}
    k=0

    with open("community.dat","r") as f:
        for line in f.readlines():
            items=line.strip("\r\n").split("\t")
            v=items[0]
            label=items[1]
            nodes_labels[v]=label
        #end-for
    #end-with

    G=nx.Graph()
    for v in nodes_labels.keys(): #添加所有的节点，并且记录其真实标签
        G.add_node(v, value=nodes_labels[v])

    edges=set()

    with open("network.dat","r") as f:
        for line in f.readlines():
            items=line.strip("\r\n").split("\t")
            a=items[0]
            b=items[1]
            if (a,b) not in edges or (b,a) not in edges:
                edges.add( (a,b) )
        #end-for
    #end-with

    for e in edges:
        a,b=e
        G.add_edge(a,b,type="Undirected")

    nx.write_gml(G,"../dataset/LFR.gml")
    print ("transfer LFR(*.dat) data to *.gml")

    communities=defaultdict(lambda :[])
    for v in nodes_labels.keys():
        label=nodes_labels[v]
        communities[label].append(v)

    for c in communities.keys():
        print ("community ", c ,": \n", communities[c], "\n")

def main():
    transfer_2_gml()

if __name__ == '__main__':
    main()