# encoding:utf-8
import os
import time

statinfo = os.stat(r"E:\SP\1.1\dataset\karate.csv")
a = time.localtime(statinfo.st_ctime)
print "年:" + str(a[0])
print "月:" + str(a[1])
print "日:" + str(a[2])
print  a[3]
print  a[4]
print  a[5]
