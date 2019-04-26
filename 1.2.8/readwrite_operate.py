# encoding:utf-8

import csv
import matplotlib.pyplot as plt
import networkx as nx
import os

def read_graph_csv(file):
    '''
    输入：csv边集文件
    输出：图
    '''
    csv_file = csv.reader(open(file,'r'))
    a_list = []
    G = nx.Graph()

    for row in csv_file:
        if csv_file.line_num == 1:                      #忽略第一行
            continue
        a = []
        a.append(int(row[0]))
        a.append(int(row[1]))
        a_list.append(a)

    G.add_edges_from(a_list)

    return G

def read_gml(gml_file):
    G = nx.read_gml(open(gml_file))
    nx.draw_networkx(G)
    plt.show()

    return G

def save_graph_csv(graph, filepath):
    '''
    :param graph: 图
    :param filepath: 文件名不包括后缀名
    :return:
    '''
    d = list(graph.edges())
    filepath = str('../dataset/') + str(filepath) + str('.csv')
    csvFile = open(filepath, "wb")
    writer = csv.writer(csvFile)

    firstline = ["Source", "Target"]
    writer.writerow(firstline)

    for i in range(len(d)):
        writer.writerow(d[i])

    csvFile.close()
    return filepath

def save_SNV(dataDict={}, fileName="SNV_.csv"):
    fileName = '../result/' + fileName

    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)

        firstline = ["id", "SNV"]
        csvWriter.writerow(firstline)

        for k,v in dataDict.iteritems():
            csvWriter.writerow([k,v])

        csvFile.close()
        print 'SNV值已存储到' + str(fileName)

def save_single_round_result(dataDict={}, fileName="test_result.csv"):
    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)

        firstline = ["test round","max_day", "max_rate"]
        csvWriter.writerow(firstline)

        for k,v in dataDict.iteritems():
            csvWriter.writerow([k, v['max_day'], v['max_rate']])

        csvFile.close()
        print '该轮结果已存储到' + str(fileName)

def save_nodeatt(dataDict={},fileName="nodeatt.csv"):
    '''
    存储节点的NCC、VAR、SPIG三个值到csv
    :param dataDict:
    :param fileName:
    :return:
    '''
    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)

        for k,v in dataDict.iteritems():
            csvWriter.writerow([k,v['NCC'],v['VAR'],v['SPIG']])

        csvFile.close()
        print 'nodeatt值已存储到nodeatt.csv'

def save_final_result(dataDict={},fileName="../result/final_compare"):
    '''
        根据最后的实验数据绘制多个算法的情况比较图和输出csv
        :param dataDict:
        :param fileName:
        :return:
        '''
    ratepng = fileName + '.png'
    csvpath = fileName + '.csv'
    plt.close()
    day_row = []
    rate_row = []
    source_num = []
    day_table = {}
    rate_table = {}
    line_style = {1:'b^-', 2:'rd-', 3:'gs-', 4:'yp-', 5:'mo-', 6:'xk-', 7:'c+-' }  # 折线图样式
    line_num = 1  # 折线图样式循环递增变量

    # 将SIRmain输出的数据分类提取出来
    for key_1, value_1 in dataDict.iteritems():
        source_num = []
        for key_2 in value_1:
            rate_row.append(key_2[0])
            day_row.append(key_2[1])
            source_num.append(key_2[2])
        day_table[key_1] = day_row
        rate_table[key_1] = rate_row

        day_row = []  # 清空单个数据的值，为下一组数据重新准备
        rate_row = []

    # 绘制感染天数折线图
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['figure.figsize'] = (10, 4.0)
    plt.subplot(122)
    for k in day_table:
        plt.plot(source_num, day_table[k], line_style[line_num], label=str(k))
        line_num += 1
    plt.xlabel(u"top-k源节点数量")
    plt.ylabel(u"达到最大感染率所需时间/周期")
    plt.legend()

    # 绘制最大感染率折线图
    plt.subplot(121)
    line_num = 1
    for k in day_table:
        plt.plot(source_num, rate_table[k], line_style[line_num], label=str(k))
        line_num += 1
    plt.xlabel(u"top-k源节点数量")
    plt.ylabel(u"最大感染率/%")
    plt.legend()

    plt.savefig(ratepng, dpi=300)

    #存储csv文件
    with open(csvpath, "wb") as f:
        f.write('The maximum rate of infection with the number of different source nodes.')
        f.write('\n')
        first_line = ','
        for i in source_num:
            first_line = first_line + str(i) + ','
        f.write(first_line)
        f.write('\n')
        for k in rate_table:
            next_line = k + ','
            for i in rate_table[k]:
                next_line = next_line + str(i) + ','
            f.write(next_line)
            f.write('\n')
        f.write('\n')
        f.write('The time of reach the maximum infection Rate.')
        f.write('\n')
        first_line = ','
        for i in source_num:
            first_line = first_line + str(i) + ','
        f.write(first_line)
        f.write('\n')
        for k in day_table:
            next_line = k + ','
            for i in day_table[k]:
                next_line = next_line + str(i) + ','
            f.write(next_line)
            f.write('\n')

    print '---------------------'
    print '最终实验结果已存储:'
    print csvpath
    print ratepng
    return

def namepathmix(graph_name='', alg_name='', num=None, k=None):
    '''
    生成对应的文件夹路径，文件名称
    :param graph_name:
    :param alg_name:
    :param num:
    :param k:
    :return:
    '''
    namepath = {}
    namepath['pngname'] = graph_name + '_' + alg_name + '_' + str(num) + '_' + str(k) + '.png'
    namepath['pngpath'] = '../result/' + graph_name + '/' + alg_name + '_' + str(num) + '/' + namepath['pngname']
    namepath['finalpath'] = '../result/' + graph_name + '/' + 'final_compare'
    namepath['csvpath'] = '../result/' + graph_name + '/' + alg_name + '_' + str(num) + '/' + 'result.csv'
    namepath['graphpath'] = '../dataset/' + graph_name + '.csv'
    namepath['valuepath'] = '../result/' + graph_name + '_' + alg_name + '.csv'
    namepath['subfolder'] = '../result/' + graph_name + '/' + alg_name + '_' + str(num) + '/'
    return namepath

def create_folder(graph_name, alg_name, num):
    '''
    在生成保存文件前先创建文件夹
    :param graph_name:
    :param alg_name:
    :param num:
    :return:
    '''
    folder_paths = namepathmix(graph_name, alg_name, num)
    path = folder_paths['subfolder']
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径

if __name__ == '__main__':
    graph_A = read_graph_csv('../dataset/lesmis.csv')
    # graph_B = read_graph_csv('../dataset/karate.csv')

    print ("nodes of graph_dolphins:", graph_A.number_of_nodes())
    # print ("edges of graph_karate:", graph_B.edges())


    nx.draw_networkx(graph_A)
    plt.show()

    # save_graph_csv(graph_A, 'asd')