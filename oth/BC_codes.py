# encoding:utf-8


import networkx as nx
# import matrix_operate as mato
from Queue import Queue
import readwrite_operate as rwo

# G = nx.random_graphs.barabasi_albert_graph(100,3)
# #algorithm from networkx

# G = rwo.read_graph_csv('../dataset/karate.csv')
#
G = nx.Graph()
G.add_edges_from(
    [(1, 2), (1, 4), (2, 3), (3, 4), (4, 5), (5, 6), (5, 8), (6, 7), (7, 8)])



# C = nx.centrality.betweenness_centrality(G,normalized=False)

CB = dict.fromkeys(G,0.0)                       #初始化中介中心性值为0
for s in G.nodes():                             #依次将节点作为源节点
    Pred = {w:[] for  w in G.nodes()}           #初始化前序节点集
    dist = dict.fromkeys(G,None)                #初始化最短路径为‘None’
    sigma = dict.fromkeys(G,0.0)                #初始化σ值
    dist[s] = 0                                 #源节点的距离初始化为0
    sigma[s] = 1                                #最短路径条数初始化为1
    Q = Queue()                                 #用于广度优先搜索的队列
    Q.put(s)                                    #将源节点加入到队列中
    S = []                                      #初始化空堆，用于寻找s的连通片
    while not Q.empty():                       #如果队列Q不为空
        v = Q.get()                             #从队列Q中取出一个节点v
        S.append(v)                             #将v加入到堆S中，加入到s的连通片中
        for w in G.neighbors(v):               #取出v的所有邻接点
            if dist[w] == None:                 #如果s到w还没计算过，没计算过的用‘None’表示
                dist[w] = dist[v] + 1           #则初始化d(s,w)=d(s,v)+1
                Q.put(w)                        #取出w放入队列Q中
            if dist[w] == dist[v] + 1:          #如果d(s,w)=d(s,v)+1，也就是s到w的最短路径经过v
                sigma[w] += sigma[v]            #那么s到w的最短路径数需要加上经过v的最短路径数
                Pred[w].append(v)               #并将v加入到w的前序节点集中
    delta = dict.fromkeys(G,0.0)                #初始化所有节点依赖于s的中介中性值
    for w in S[::-1]:                          #当S不为空时
        for v in Pred[w]:                       #取出w的前序节点集合，依次计算其相对于s源节点的中介中心性
            delta[v] += sigma[v]/sigma[w]*(1+delta[w])
        if w != s:                              #将w的依赖中介中心性值归总到其中介中心性上
            CB[w] += delta[w]

    print str(s) + ':' + str(dist)

for v in CB:
    CB[v] /= 2.0


print CB


#compare with networkx's implements 
# print(sum(abs(CB[v]-C[v]) for v in G)) #1.59428026336e-13

# print CB