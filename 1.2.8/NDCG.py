# encoding:utf-8

import csv
import os
import math
from operator import itemgetter

def getDCG(rank):
    dcg = 0
    i = 1
    for key in rank[0:]:
        dcg = dcg + (pow(2, key)-1) / math.log(i+1,2)           #另一种常用的DCG（折损累计增益）计算方法：这个主要体现越靠前的越重要
        # dcg = dcg + key / math.log(i, 2)                    #该计算方法以人工标注的分数进行计算
        i = i + 1
    return dcg

def getIDCG(ranking):
    ranking.sort(reverse=True)
    return getDCG(ranking)

def getNDCG_manual(real, standard):
    '''
    手工计算两个排序结果的NDCG分数
    :param real: 实际排序结果
    :param standard: 标准排序结果
    :return: NDCG分数
    '''
    NDCG = 0
    DCG = getDCG(real)
    iDCG = getIDCG(standard)

    print 'DCG = ' + str(DCG)
    print 'iDCG = ' + str(iDCG)
    print 'NDCG = ' + str(DCG / iDCG)

    return NDCG

def sorted_value(file):
    input_file = open(file)
    output_file = open('sorted_temp.csv', "wb")

    table = []
    header = input_file.readline()
    for line in input_file:
        col = line.split(',')
        table.append(col)

    table_sorted = sorted(table, key=itemgetter(1), reverse=True)

    for row in table_sorted:
        row = [str(x) for x in row]
        output_file.write(",".join(row))

    input_file.close()
    output_file.close()

    return 'sorted_temp.csv'

def read_topk_list(file,type,topk):
    '''
    按SDGI值的顺序读取top50节点编号,并根据顺序赋予初始位置递减分数
    :param file: 生成的sorted_SDGI.csv文件
    :param type: 输入的
    :param topk: 取前topk位进行计算比较
    :return: 节点编号顺序list
    '''
    sort_file = sorted_value(file)                          #首先对SPIG.csv排序
    csv_file = csv.reader(open(sort_file,'r'))
    key = topk
    topk_nodes = [[0,0]]                       #[key-[node,score]]用0先填充0号位置的数据，便于后面一一对应

    for row in csv_file:
        topk_nodes_item = []
        if key > 0:
            topk_nodes_item.append(int(row[0]))

            if type == 'standard':                   #赋予标准list初始位置递减分数
                topk_nodes_item.append(key)
            elif type == 'BCFilter':                 #初始化过滤后list的分数为0，便于后期更新区分标准list中没有出现的节点
                topk_nodes_item.append(0)

            topk_nodes.append(topk_nodes_item)
            key -= 1
        else:break

    return topk_nodes

def NDCG_BCFilter(standard_file, BCFilter_file, topk=50):
    '''
    计算BC过滤后，getSPIG_NCC_VAR.csv中top50节点的一致性
    :param standard_file: 未过滤的SPIG.csv文件
    :param BCFilter_file: BC过滤后的SPIG.csv文件
    :return: NDCG分数
    '''
    BCFilter_top50_list = read_topk_list(BCFilter_file,'BCFilter',topk)     #将BC过滤后的SPIG.csv文件中前50个节点存为list
    standard_top50_list = read_topk_list(standard_file,'standard',topk)     #将标准的SPIG.csv文件中前50个节点存为list

    os.remove('sorted_temp.csv')

    k = len(BCFilter_top50_list)

    for i in range(1,k):
        for j in range(1,k):
            if BCFilter_top50_list[i][0] == standard_top50_list[j][0]:      #如果BC过滤后的list中的元素出现在标准list中就将其分数更新
                BCFilter_top50_list[i][1] = standard_top50_list[j][1]
            else: continue

    DCG = 0
    IDCG = 0
    NDCG = 0

    for i in range(1,k):                                                        #开始分别累加计算DCG和IDCG值
        DCG = DCG + BCFilter_top50_list[i][1] / math.log(i+1, 2)                #基础打分计算
        IDCG = IDCG + (k-i) / math.log(i+1, 2)
        #
        # DCG = DCG + pow(2, BCFilter_top50_list[i][1]) / math.log(i + 1, 2)    #2的指数打分计算，排序越靠前的节点越重要
        # IDCG = IDCG + pow(2, (k - i)) / math.log(i + 1, 2)

        NDCG = DCG / IDCG

    return NDCG

if __name__ == '__main__':

    # a = NDCG_BCFilter('../result/coauthor_SNV-BC82.csv', '../result/coauthor_SNV-BC28.csv', 50)
    # b = NDCG_BCFilter('../result/dolphins_SNV.csv', '../result/dolphins_SNV-BC.csv', 40)
    # c = NDCG_BCFilter('../result/dolphins_SNV.csv', '../result/dolphins_SNV-BC.csv', 30)
    # d = NDCG_BCFilter('../result/dolphins_SNV.csv', '../result/dolphins_SNV-BC.csv', 20)
    # e = NDCG_BCFilter('../result/dolphins_SNV.csv', '../result/dolphins_SNV-BC.csv', 10)

    # print 'NDCG@50: ' + str(a)
    # print 'NDCG@40: ' + str(b)
    # print 'NDCG@30: ' + str(c)
    # print 'NDCG@20: ' + str(d)
    # print 'NDCG@10: ' + str(e)


    # 手工计算比较两个序列----------------------------------
    real_rank_scores = [6,5]        # 每条搜索结果的人工标注分数
    standard_rank_scores = [8,7]

    getNDCG_manual(real_rank_scores, standard_rank_scores)






