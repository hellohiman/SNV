# encoding:utf-8

import networkx as nx
import matplotlib.pyplot as plt
# WS network
# generate a WS network which has 20 nodes,
# each node has 4 neighbour nodes,
# random reconnection probability was 0.3.
WS = nx.random_graphs.watts_strogatz_graph(20, 4, 0.3)
WS.remove_node(0)
# circular layout
pos = nx.spectral_layout(WS)

nx.write_gexf(WS, 'your_file_name.gexf')    #将图存储为gephi文件

nx.draw(WS, pos, with_labels = True, node_size = 20)
plt.show()