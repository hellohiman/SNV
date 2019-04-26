# encoding:utf-8

import matplotlib.pyplot as plt
import numpy as np

font1 = {'family': 'SimHei', 'weight': 'normal', 'size': '10'}

def benchmark1_NDCGscores():
    '''
    benchmark1网络中各算法的NDCG评分对比图
    :return:
    '''
    size = 4
    x = np.arange(size)
    SNV_BC = [0.668, 0.760, 0.787, 0.790]
    PR = [0.163, 0.292, 0.540, 0.544]
    BC = [0.668, 0.791, 0.795, 0.795]
    CC = [0.246, 0.697, 0.682, 0.685]
    HCC = [0.216, 0.670, 0.687, 0.691]

    total_width, n = 0.8, 5  # 有多少个类型，只需更改n即可
    width = total_width / n
    x = x - (total_width - width) / 2

    # 添加图形属性
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签
    # plt.xlabel('NDCG@n', fontsize='large')
    plt.ylabel('NDCG score', fontsize='large')
    # plt.title('NDCG@n ranking_scores comparison')
    plt.xticks(x + 2 * width, ('NDCG@2', 'NDCG@4', 'NDCG@6', 'NDCG@8'))
    plt.ylim(0, 1.0)

    plt.bar(x, HCC, width=width, label='HCC')
    plt.bar(x + width, CC, width=width, label='CC')
    plt.bar(x + 2 * width, PR, width=width, label='PR')
    plt.bar(x + 3 * width, BC, width=width, label='BC')
    plt.bar(x + 4 * width, SNV_BC, width=width, label='SNV-BC')

    # 添加对应数据值
    for x,a,b,c,d,e in zip(x,HCC,CC,PR,BC,SNV_BC):
        plt.text(x + 0 * width, a, '%.2f' % a, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 1 * width, b, '%.2f' % b, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 2 * width, c, '%.2f' % c, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 3 * width, d, '%.2f' % d, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 4 * width, e, '%.2f' % e, ha='center', va='top', rotation=90, color='white', fontdict=font1)

    plt.legend(ncol=5)
    plt.savefig('../result/benchmark1_NDCGscores.png', dpi=200)
    plt.show()

def BCFilter_NDCG_comparison():
    '''
    过滤后不同网络中top50节点的相似性评分图
    :return:
    '''
    size = 7
    ndcg_score_50 = [1.000, 0.997, 1.000, 0.976, 0.9519, 0.9540, 0.8912]
    ndcg_score_40 = [1.000, 1.000, 1.000, 0.990, 0.9748, 0.9784, 0.8948]
    ndcg_score_30 = [1.000, 1.000, 1.000, 0.997, 0.9889, 0.9902, 0.8869]
    ndcg_score_20 = [1.000, 1.000, 1.000, 1.000, 1.0000, 1.0000, 0.8796]
    ndcg_score_10 = [1.000, 1.000, 1.000, 1.000, 1.0000, 1.0000, 0.8167]
    x = np.arange(size)

    plt.ylim(0, 1.2)

    total_width, n = 0.8, 6  # 有多少个类型，只需更改n即可
    width = total_width / n
    x = x - (total_width - width) / 2

    plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签
    # plt.title(u'BC过滤前后不同网络中top50节点的NDCG评分（满分：1）')
    # plt.xlabel(u'不同网络', fontsize='large')
    plt.ylabel(u'NDCG scores', fontsize='large')
    plt.xticks(x+ 2.5 * width, ('zachary', 'dolphins', 'coauthor', 'LFR-500', 'LFR-1000', 'LFR-1500', 'LFR-2000'))

    plt.bar(x, ndcg_score_10, width=width, label=u'top10')
    plt.bar(x + 1 * width, ndcg_score_20, width=width, label=u'top20')
    plt.bar(x + 2 * width, ndcg_score_30, width=width, label=u'top30')
    plt.bar(x + 3 * width, ndcg_score_40, width=width, label=u'top40')
    plt.bar(x + 4 * width, ndcg_score_50, width=width, label=u'top50')

    for x, y1,y2,y3,y4,y5 in zip(x, ndcg_score_10,ndcg_score_20,ndcg_score_30,ndcg_score_40,ndcg_score_50):
        plt.text(x + 0 * width, y1, '%.3f' % y1, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 1 * width, y2, '%.3f' % y2, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 2 * width, y3, '%.3f' % y3, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 3 * width, y4, '%.3f' % y4, ha='center', va='top', rotation=90, color='white', fontdict=font1)
        plt.text(x + 4 * width, y5, '%.3f' % y5, ha='center', va='top', rotation=90, color='white', fontdict=font1)

    plt.legend(ncol=5)
    plt.savefig('../result/BCFilter_NDCG_comparison.png', dpi=200, figsize=(12, 5))

    plt.show()

    return None

def time_comparison():
    '''
    优化前后的算法运行时间对比折线图
    :return:
    '''
    node_nums = [34, 63, 100, 200, 500, 1000, 1500, 2000]
    time_before_filter = [0.15, 0.64, 4.4, 33, 580, 4300, 15397, 40283]
    # time_after_filter = [0.001, 0.049, 0.12, 0.9, 15.17, 117.49, 409.54, 933.23]
    time_after_filter = [0.001, 0.049, 0.12, 0.9, 54.46, 220.49, 502.54, 889.82]

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.title(u'BC过滤前后计算时间对比', fontsize='x-large')
    plt.xlabel(u'数据集规模', fontsize='large')
    plt.ylabel(u'算法运行时间 (×千秒)',fontsize='large')
    plt.plot(node_nums, time_before_filter, 'rd-', label=u"SNV")
    plt.plot(node_nums, time_after_filter, 'g^-', label=u"SNV-BC")

    plt.yticks([5000,10000,15000,20000,25000,30000,35000,40000],
               [5,10,15,20,25,30,35,40])

    for i in range(4,8):
        plt.text(node_nums[i], time_before_filter[i], '%.2f' % (time_before_filter[i]/1000), ha='right', va='bottom')
        plt.text(node_nums[i], time_after_filter[i], '%.2f' % (time_after_filter[i]/1000), ha='center', va='top')

    plt.legend(fontsize='large')
    # plt.grid(True)

    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

    plt.savefig('../result/algorithm_time_comparison.png', dpi=200, pad_inches = 0)
    plt.show()

    return None

if __name__ == '__main__':
    benchmark1_NDCGscores()

    # BCFilter_NDCG_comparison()

    time_comparison()