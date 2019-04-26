# coding=utf-8

import csv

def PersonalPageRank(G, alpha, root, max_step):
    rank = dict()
    rank = {x: 0 for x in G.keys()}
    rank[root] = 1
    # 开始迭代
    for k in range(max_step):
        tmp = {x: 0 for x in G.keys()}
        # 取节点i和它的出边尾节点集合ri
        for i, ri in G.items():
            # 取节点i的出边的尾节点j以及边E(i,j)的权重wij, 边的权重都为1，在这不起实际作用
            for j, wij in ri.items():
                # i是j的其中一条入边的首节点，因此需要遍历图找到j的入边的首节点，
                # 这个遍历过程就是此处的2层for循环，一次遍历就是一次游走
                tmp[j] += alpha * rank[i] / (1.0 * len(ri))
        # 我们每次游走都是从root节点出发，因此root节点的权重需要加上(1 - alpha)
        # 在《推荐系统实践》上，作者把这一句放在for j, wij in ri.items()这个循环下，我认为是有问题。
        tmp[root] += (1 - alpha)
        rank = tmp

        # 输出每次迭代后各个节点的权重
        print 'iter: ' + str(k) + "\t",
        for key, value in rank.items():
            print "%s:%.5f, \t" % (key, value),
        print

    return rank


def exchange_graph_datastructure(file):
    '''
    将边集合图结构转换为字典结构的图
    输入：csv边集图
    输出：字典结构的图
    '''
    csv_file = csv.reader(open(file,'r'))
    Graph = {}

    for row in csv_file:
        if csv_file.line_num == 1:                      #忽略第一行
            continue

        if row[0] not in Graph:
            Graph[row[0]] = {}

            if row[1] not in Graph:
                Graph[row[1]] = {}

            Graph[row[0]][row[1]] = 1
            Graph[row[1]][row[0]] = 1
        else:
            if row[1] not in Graph:
                Graph[row[1]] = {}

            Graph[row[0]][row[1]] = 1
            Graph[row[1]][row[0]] = 1

    return Graph

def save_rankvalue(dataDict={}, fileName="SNV_.csv"):
    fileName = '../result/' + fileName

    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)

        firstline = ["id", "PersonalPageRank"]
        csvWriter.writerow(firstline)

        for k,v in dataDict.iteritems():
            csvWriter.writerow([k,v])

        csvFile.close()
        print 'PersonalRank值已存储到' + str(fileName)

def run(Name):
    namepath = '../dataset/' + Name + '.csv'
    filename = Name + '_PPR.csv'
    G = exchange_graph_datastructure(namepath)

    PRvalue = PersonalPageRank(G, 0.85, '1', 100)

    save_rankvalue(PRvalue, filename)

if __name__ == '__main__':

    dataset = ['LFR500', 'LFR1000', 'LFR1500', 'LFR2000', 'coauthor', 'zachary', 'dolphins']
    for item in dataset:
        run(item)
