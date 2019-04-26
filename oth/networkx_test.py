
# encoding:utf-8

import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_node(1)
G.add_edges_from([(1,2),(1,3),(3,2)])

if (1,4) in G.edges():
    print 'yes'

# G.add_node("spam")
# G.add_nodes_from("abc")
# G.add_edge('e',1)
# G.add_edge('e','spam')

# G.remove_node(1)
print G.degree(1)   #节点1的度
print nx.degree_histogram(G)  #返回图中所有节点的度分布序列（从0至最大度的出现频次）


print "num of nodes:" , G.number_of_nodes()
print "num of edges:",G.number_of_edges()
print "nodes of graph:",G.nodes()
print "edges of graph:",G.edges()
print "edges of node '1' graph:",G.edges(1)
print "the neighbor of node 1 is:",G.neighbors(1)

a = nx.number_connected_components(G)       #连通分量个数

nx.draw_networkx(G,node_size=10)
plt.show()

plt.colors()

# nx.draw(G)
# plt.savefig("path.png")

#将图保存为gml文件
# nx.write_gml(G, 'dataset/aaaa.gml')

#networkx 中图格式类型数据的求两点间的最短路径
# path = nx.shortest_path_length(G, start, end)  # 求最短路径长度