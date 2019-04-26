# encoding:utf-8

import time
import readwrite_operate as rwo
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from Queue import Queue

#全局变量（逻辑需要）---------------------------------------------
time_list = []                               #用于统计累加算法核心各段的时间
remove_list = []                             #用于记录优化移除的节点，便于后期补入
fileinfo = {}                                #图文件名

#全局变量（节省时间成本需要）---------------------------------------------
dist = {}                                    #图对应的最短路径字典表，用作全局是为了节省时间成本，避免多次计算
G = nx.Graph()                               #图，读取图文件后，直接存为全局变量，避免后期多次读图

def BC_SP(graph):
    '''
    提取自BC中的最短路径计算代码
    计算图中任意两个节点对间的最短路径
    :param graph:
    :return:list: dict:最短路径表，字典嵌套字典，字典值是每个节点到所有节点的最短路径
    '''
    dist_temp = {}
    for s in graph.nodes():                     # 依次将节点作为源节点
        s_dist = dict.fromkeys(graph, None)     # 初始化最短路径为‘None’
        s_dist[s] = 0                           # 源节点的距离初始化为0
        Q = Queue()                             # 用于广度优先搜索的队列
        Q.put(s)                                # 将源节点加入到队列中
        while not Q.empty():                    # 如果队列Q不为空
            v = Q.get()                         # 从队列Q中取出一个节点v
            for w in graph.neighbors(v):        # 取出v的所有邻接点
                if s_dist[w] == None:           # 如果s到w还没计算过，没计算过的用‘None’表示
                    s_dist[w] = s_dist[v] + 1   # 则初始化d(s,w)=d(s,v)+1
                    Q.put(w)                    # 取出w放入队列Q中
        dist_temp[s] = s_dist
    return dist_temp

def Vertex_SP(dict):
    '''
    计算单源节点的最短路径和
    :param dict:该节点到其他节点的最短路径（字典值）
    :return:最短路径和（int）
    '''
    sum_temp = 0
    for i in dict:
        if dict[i] != None:
            sum_temp += dict[i]
    return sum_temp

def Network_SP(dist):
    '''
    计算图最短路径和
    :param dist: 最短路径表
    :return: 图的最短路径和（int）
    '''
    sum_dist = 0
    for key in dist:
            sum_single = Vertex_SP(dist[key])
            sum_dist += sum_single
    return sum_dist

def getSPIG_NCC_VAR(graph, node):
    '''
    计算删除节点前后的最短路径增加值
    备注：增加值=删后值-删前值    为计算方便，上述公式
          等价于 增加值 = 删后值 - （删前值 - 该节点为源节点的最短路径）
          等价于 增加值 = 删后值 + 该节点为源节点的最短路径
    :param graph:图
    :param node:删除的节点
    :return:dict:单个的节点三属性字典
    '''

    M = nx.Graph()                                      #复制图，并用复制后的图进行删点操作，避免后续需要重复读图
    M.add_edges_from(graph.edges())

    node_info = {}.fromkeys(['NCC','VAR','SPIG'])       #NCC(number_connected_components):子连通分量个数.VAR(variance):方差])

    start_time = time.time()

    M.remove_node(node)             #删除对应节点

    NCC_value = nx.number_connected_components(M)

    if (NCC_value == 1):

        SPG_before_instead = Vertex_SP(dist[node])                 # 计算删前SPG代替值  该节点为源节点的最短路径
        dist_after_remove = BC_SP(M)                    # 计算删后的SPG值
        SPG_after = Network_SP(dist_after_remove)
        SPIG_value = SPG_after + SPG_before_instead                   #SDG增加值的替代值

        node_info.update(NCC=1, VAR=0 , SPIG=SPIG_value)

    elif (NCC_value > 1):                           #产生多个子连通分量时，就记录子连通分量个数NCC和各个子连通分量节点数的方差VAR
        NN = []
        a = nx.connected_components(M)
        for i in a:
            NN.append(len(i))              #将各个子连通分量节点数加入到数组NN中便于计算方差
            VAR_value = np.var(NN)         #计算节点数方差
        node_info.update(NCC=NCC_value, VAR=VAR_value, SPIG=0)

    end_time = time.time()
    run_time = end_time - start_time
    time_list.append(run_time)

    return node_info

def optimize_graph(graph):
    '''
    图优化
    删除图中度为1的节点，以及度为2且其两个邻接点间有边的节点
    :param graph: 待处理图
    :return: graph：处理后的图
    '''
    s_time = time.time()

    for i in range(0, graph.number_of_nodes()):

        if graph.degree(i) == 1:
            graph.remove_node(i)
            remove_list.append(i)

    e_time = time.time()
    r_time = e_time - s_time
    time_list.append(r_time)

    return graph

def SNV_valuefill(dic):
    '''
    补全SNV_list中被优化节点数据'0'
    :param dic: SNV_dic
    :return: dic:补全的SNV_dic
    '''
    for key in remove_list: dic[key] = 0
    return dic

def norm_merge_3att(dict):
    '''
    将节点属性中的三个值归一化，这里的归一化是排除0的
    :param dict: 节点属性字典
    :return: dict：归一化的节点属性字典
    '''
    min_ncc = 999999999999999
    min_var = 999999999999999
    min_spig = 999999999999999
    max_ncc = 0
    max_var = 0
    max_spig = 0
    norm_merge = {}

    for key in dict:
        node_ncc = dict[key]['NCC']
        if max_ncc < node_ncc: max_ncc = node_ncc
        if min_ncc > node_ncc and node_ncc != 0: min_ncc = node_ncc

        if dict[key]['VAR'] != 0:                   #VAR是负相关，取其倒数参与归一化，该操作是为排除0不可以做除数的影响
            node_var = 1/float(dict[key]['VAR'])
            if max_var < node_var: max_var = node_var
            if min_var > node_var and node_var != 0: min_var = node_var

        node_spig = dict[key]['SPIG']
        if max_spig < node_spig: max_spig = node_spig
        if min_spig > node_spig and node_spig != 0: min_spig = node_spig

    min_spig = min_spig - 1         #这个需要注意：最小值再下探1，主要是为了避免SPIG最小的节点与度为1的节点混在一起
    min_ncc = min_ncc - 1
    min_var = min_var - 1
    ncc_gap = max_ncc - min_ncc
    var_gap = max_var - min_var
    spig_gap = max_spig - min_spig

    for key in dict:
        temp = {}.fromkeys(['NCC','VAR','SPIG'])
        node_ncc = dict[key]['NCC']

        if dict[key]['VAR']!=0:                         #VAR是负相关，取其导数参与归一化，该操作是为排除0不可以做除数的影响
            node_var = 1/float(dict[key]['VAR'])
        else:node_var = 0

        node_spig = dict[key]['SPIG']
        if node_ncc!=0:
            temp['NCC'] = (float(node_ncc) - min_ncc) / ncc_gap
        else:temp['NCC'] = 0.0
        if node_var!=0:
            temp['VAR'] = (float(node_var) - min_var) / var_gap
        else:temp['VAR'] = 0.0
        if node_spig!=0:
            temp['SPIG'] = (float(node_spig) - min_spig) / spig_gap
        else:temp['SPIG'] = 0.0

        norm_merge[key] = 0.2 * temp['NCC'] + 0.8 * (temp['VAR'] +  temp['SPIG'])

    return norm_merge

def file(name):
    path = '../dataset/'+ name +'.csv'
    fileinfo['name'] = name + '_SNV-BC.csv'           #将SPIG最终文件名存储到全局变量fileinfo中便于后期调用
    return path

def BC_filtering(graph):
    filtering_list = []

    C = nx.centrality.betweenness_centrality(graph, normalized=False)

    sorted_key_list = sorted(C, key=lambda x:C[x])                          # 顺序排列，从小到大排列
    # sorted_key_list = sorted(C, key=lambda x: C[x], reverse=True)         # 倒序排列，从大到小
    sorted_dict = map(lambda x: {x: C[x]}, sorted_key_list)

    if graph.number_of_nodes() <2000 :
        n = graph.number_of_nodes() - 50                        #最低节点数不低于50
    else:
        n = int( graph.number_of_nodes() * (1-0.025))           #超过2000个节点的网络，取前2.5%的节点

    for i in range(0, n):
        s = int(sorted_dict[i].keys()[0])
        remove_list.append(s)

    return filtering_list

if __name__ == '__main__':

    G = rwo.read_graph_csv(file('coauthor'))

    G = optimize_graph(G)                           #优化图
    BC_filtering(G)                                 #BC过滤
    print remove_list                               #优化、BC过滤后删除的节点存为全局变量，便于后续寻找节点

    dist = BC_SP(G)                                 #计算优化后的最短路径表，并作为全局常量，避免后续重复计算

    node_3att = {}
    for key in dist:                                #遍历计算各个节点三属性值
        if key not in remove_list:
            node_3att[key] = getSPIG_NCC_VAR(G, key)
        else:continue

    node_att = norm_merge_3att(node_3att)           #归一化、合并节点三属性值
    rwo.save_nodeatt(node_3att,'att.csv')

    SNV_list = SNV_valuefill(node_att)              #补缺删除的节点属性值为0
    rwo.save_SNV(SNV_list, fileinfo['name'])      #SPIG值保存到文件
    run = sum(time_list)
    print run


