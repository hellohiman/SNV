# encoding:utf-8

import csv
import readwrite_operate as rwo
import copy
import numpy as np
import matplotlib.pyplot as plt
import os
from operator import itemgetter
from random import randint

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

def read_topk(file):
    '''
    按SDGI值的顺序读取节点编号
    :param file:生成的sorted_SDGI.csv文件
    :return: 节点编号顺序list
    '''
    sort_file = sorted_value(file)
    csv_file = csv.reader(open(sort_file,'r'))
    topk_nodes = {}
    key = 0

    for row in csv_file:
        topk_nodes[key] = row[0]
        key = key + 1

    return topk_nodes

def init_SIR(graph, top, graph_name, alg_name):
    '''
    SIR扩散前的初始化，将所有节点的状态置为‘S’，将指定的topk节点状态置为‘I’
    :param top: topk的前num个作为扩散源
    :return: 返回状态字典state
    '''
    valuefile = rwo.namepathmix(graph_name,alg_name)
    a = read_topk(valuefile['valuepath'])
    state = {}

    for key in range(0,graph.number_of_nodes()):
        state[key] = 'S'                #将所有节点先置为初始S未感染状态

    for i in range(0, top):
        state[int(a[i])] = 'I'          #将前top个节点状态置为I感染态

    return state

def getRate(state,factor):
    '''
    计算当前状态感染率等
    :param state: 当前状态
    :return: float比率
    '''
    n = 0
    for key in state:
        # if state[key] == 'I' or state[key] == 'R': n = n+1
        if state[key] == factor:
            n = n + 1
    rate = float(n)/len(state)*100

    return rate

def SIR_simple(G, topk, graph_name=None, alg_name=None, roundtimes=1):
    '''
    SIR感染模拟，最终输出最大感染率和对应时间
    :param G:  图
    :param top_k: 初始加入的节点数量
    :param graph_name:  图名称
    :param alg_name: 算法名称
    :param roundtimes: 计算的轮数
    :return: 最大感染率和对应时间
    '''
    day = 0
    increaseflag = True
    pre = init_SIR(G, topk, graph_name, alg_name)            #初始化SIR三状态
    now = copy.deepcopy(pre)
    finalinfo = {}.fromkeys(['max_rate','max_day'])

    while (increaseflag == True):
        day = day + 1
        for i in pre:
            if pre[i] == 'I':
                for j in G.neighbors(i):        #循环遍历I状态节点的邻接点，若是S状态，就以alpha概率感染为I状态
                    if pre[j] == 'S':
                        alpha = float(randint(0, 100))/100
                        if (alpha<0.8) : now[j] = 'I'

                Beta = float(randint(0, 100))/100
                if (Beta<0.5) : now[i] = 'R'        #当前已感染的节点以beta的概率康复并免疫为R状态

        rate_now = getRate(now,'I')
        rate_pre = getRate(pre,'I')
        rate_gap = rate_now - rate_pre
        if rate_gap<=0: increaseflag = False         #后续需要快速计算得到最大感染率时用这个，可以提前结束循环

        if  finalinfo['max_rate'] < rate_now:        #记录最大感染率和对应的时间
            finalinfo['max_rate'] = rate_now
            finalinfo['max_day'] = day

        pre = copy.deepcopy(now)        #完成一轮遍历，当前状态置为前序状态

    return finalinfo

def SIR_view(G, topk, graph_name=None, alg_name=None, roundtimes=1):
    '''
    SIR感染模拟，绘制整个感染过程变化情况坐标图
    :param G: 图
    :param topk: 初始加入的节点
    :param valuefile: 对应SNV值文件的文件名
    :param roundtimes: 用于控制循环对图片文件编号
    :return: 最大感染率和对应时间
    '''
    day = 0
    increaseflag = True
    pre = init_SIR(G, topk, graph_name, alg_name)             #初始化SIR三状态
    now = copy.deepcopy(pre)
    finalinfo = {}.fromkeys(['max_rate','max_day'])
    Irate = []
    Srate = []
    Rrate = []
    dayy = []

    while (increaseflag == True):
        day = day + 1
        for i in pre:
            if pre[i] == 'I':
                for j in G.neighbors(i):        #循环遍历I状态节点的邻接点，若是S状态，就以alpha概率感染为I状态
                    if pre[j] == 'S':
                        alpha = float(randint(0, 100))/100
                        if (alpha<0.8) : now[j] = 'I'

                Beta = float(randint(0, 100))/100
                if (Beta<0.5) : now[i] = 'R'        #当前已感染的节点以beta的概率康复并免疫为R状态

        Srate_now = getRate(now, 'S')
        Irate_now = getRate(now, 'I')
        Rrate_now = getRate(now, 'R')

        if Irate_now<=0.01: increaseflag = False

        if  finalinfo['max_rate'] < Irate_now:        #记录最大感染率和对应的时间
            finalinfo['max_rate'] = Irate_now
            finalinfo['max_day'] = day

        Srate.append(Srate_now)
        Irate.append(Irate_now)
        Rrate.append(Rrate_now)

        dayy.append(day)

        pre = copy.deepcopy(now)        #完成一轮遍历，当前状态置为前序状态

    Srate_array = np.array(Srate)
    Irate_array = np.array(Irate)
    Rrate_array = np.array(Rrate)
    day_array = np.array(dayy)

    #绘制感染率变化坐标图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.plot(day_array, Srate_array, 'bs-', label=u"易感节点")
    plt.plot(day_array, Irate_array, 'ro-', label=u"感染节点")
    plt.plot(day_array, Rrate_array, 'g^-', label=u"免疫节点")
    # for a, b in zip(day_array, Irate_array):
    #     plt.text(a+0.1, b + 0.2, '%.1f%%' % b)
    plt.xlabel(u"时间")
    plt.ylabel(u"感染率/%")
    # plt.title(u"易感、感染、免疫比例变化情况")
    plt.legend(loc=0)
    # plt.grid(True)
    png_name = rwo.namepathmix(graph_name, alg_name, num=topk, k=roundtimes)
    plt.savefig(png_name['pngpath'], dpi=300)
    plt.close('all')
    print png_name['pngpath']

    return finalinfo

def SIR_single_round(graph_name, alg_name, num, roundtimes=1):
    '''
    单轮循环roundtimes次从而求出稳定的平均感染天数和最大感染率
    :param graph_name:
    :param alg_name:
    :param num:
    :param roundtimes:
    :return:
    '''
    rwo.create_folder(graph_name,alg_name,num)

    gfile = rwo.namepathmix(graph_name)
    G = rwo.read_graph_csv(gfile['graphpath'])
    test_result = {}
    ave_result = []
    temp_rate = 0.0
    temp_day = 0.0

    for i in range(1,roundtimes+1):
        irate =  SIR_simple(G, topk=num, graph_name=graph_name, alg_name=alg_name, roundtimes=i)
        # print str(i),')', irate['max_day'],'天 ',irate['max_rate']
        temp_rate = float(temp_rate) + float(irate['max_rate'])
        temp_day = float(temp_day) + float(irate['max_day'])

        test_result[i] = irate

    ave_result.append(temp_rate / roundtimes)
    ave_result.append(temp_day / roundtimes)
    ave_result.append(num)
    
    csvpath = rwo.namepathmix(graph_name,alg_name,num)
    rwo.save_single_round_result(test_result, fileName=csvpath['csvpath'])
    os.remove('sorted_temp.csv')

    return ave_result

def SIR_main(graph_name, source_node_num, Algrothims, roundtimes=50):
    '''
    多个算法的topk序列一起验证比较，并生成相应对比汇总图表
    :param graph_name: 图名称
    :param source_node_num:
    :param Algrothims:
    :param roundtimes:
    :return:
    '''
    per_numsource_rate = []
    alg_rates = {}

    for alg in Algrothims:
        for i in source_node_num:
            per_numsource_rate.append(SIR_single_round(graph_name=graph_name, alg_name=alg, num=i, roundtimes=roundtimes))   # i是感染初始节点数量,50是重复50轮求平均数,降低误差
        alg_rates[alg] = copy.deepcopy(per_numsource_rate)
        per_numsource_rate = []
    print alg_rates

    path = rwo.namepathmix(graph_name=graph_name)
    rwo.save_final_result(alg_rates, fileName=path['finalpath'])

    return

if __name__ == '__main__':

    source_node_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    Algrothims = ['SNV', 'SNV-BC', 'BC', 'CC', 'PPR', 'HCC']
    # Algrothims = ['PR', 'PPR']

    dataset = ['LFR500', 'LFR1000', 'LFR1500', 'LFR2000' ]

    for item in dataset:
        SIR_main(item, source_node_num, Algrothims, 50)


    #生成典型的SIR变化趋势图论文用-------------------
    # G = rwo.read_graph_csv('../dataset/LFR1000.csv')
    # rwo.create_folder('LFR1000', 'SNV-BC', 15)
    # SIR_view(G, topk=15, graph_name='LFR1000', alg_name='SNV-BC', roundtimes=1)

