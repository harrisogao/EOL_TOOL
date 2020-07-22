import xlrd
import xlwt

import os
import re
import threading
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

class rdCsv():
    def __init__(self):
        self.angleN7 = []
        self.angleN5 = []
        self.angleN3 = []
        self.angle3 = []
        self.angle5 = []
        self.angle7 = []
        self.range10 = []
        self.range20 = []
        self.range30 = []
        self.range40 = []
        self.range50 = []
        self.range60 = []
        self.range70 = []
        self.vlcN10 = []
        self.vlcN5 = []
        self.vlc5 = []
        self.vlc10 = []
        self.testNum = 0
        self.failedNum = 0
        self.serialNum = ""

    def writeReport(self, str):
        with open('report.doc','a') as f:
            f.write(str)

    def rdCsv(self):
        files = self.getFileName()
        counter = 0
        for i in files:
            counter = counter + 1
            with open(i, 'r') as f:
                writeFlag = 0
                for line in f.readlines():
                    uutObj = re.match(r'(.*?)UUT Serial(.*)', line, re.M | re.I)
                    if uutObj:
                        serialNum = line.split(",")
                    failedObj = re.match(r'(.*?)Failed(.*)', line, re.M | re.I)
                    if failedObj:
                        if writeFlag == 0:
                            report = "测试失败序列号:" +serialNum[1]
                            self.writeReport(report)
                            writeFlag = 1
                        self.failedNum = self.failedNum + 1
                        str = line.split(" ")
                        if str[0] != "UUT":
                            report = " case " + str[0] + "test failed" + '\n'
                            self.writeReport(report)
                            #print("case ",str[0], "test failed")
                    matchObj = re.match(r'Angle Test *', line, re.M | re.I)
                    if matchObj:
                        str = line.split(" ")
                        matchN7 = re.match(r'-7°*', str[3], 0)
                        if matchN7:
                            num = float(str[4].split(",")[1])
                            self.angleN7.append(num)
                        matchN5 = re.match(r'-5°*', str[3], 0)
                        if matchN5:
                            num = float(str[4].split(",")[1])
                            self.angleN5.append(num)
                        matchN3 = re.match(r'-3°*', str[3], 0)
                        if matchN3:
                            num = float(str[4].split(",")[1])
                            self.angleN3.append(num)
                        match3 = re.match(r'3°*', str[3], 0)
                        if match3:
                            num = float(str[4].split(",")[1])
                            self.angle3.append(num)
                        match5 = re.match(r'5°*', str[3], 0)
                        if match5:
                            num = float(str[4].split(",")[1])
                            self.angle5.append(num)
                        match7 = re.match(r'7°*', str[3], 0)
                        if match7:
                            num = float(str[4].split(",")[1])
                            self.angle7.append(num)
                    matchObj = re.match(r'Range Test *', line, re.M | re.I)
                    if matchObj:
                        str = line.split(" ")
                        range10 = re.match(r'10m*', str[3], 0)
                        if range10:
                            num = float(str[4].split(",")[1])
                            self.range10.append(num)
                        range20 = re.match(r'20m*', str[3], 0)
                        if range20:
                            num = float(str[4].split(",")[1])
                            self.range20.append(num)
                        range30 = re.match(r'30m*', str[3], 0)
                        if range30:
                            num = float(str[4].split(",")[1])
                            self.range30.append(num)
                        range40 = re.match(r'40m*', str[3], 0)
                        if range40:
                            num = float(str[4].split(",")[1])
                            self.range40.append(num)
                        range50 = re.match(r'50m*', str[3], 0)
                        if range50:
                            num = float(str[4].split(",")[1])
                            self.range50.append(num)
                        range60 = re.match(r'60m*', str[3], 0)
                        if range60:
                            num = float(str[4].split(",")[1])
                            self.range60.append(num)
                        range70 = re.match(r'70m*', str[3], 0)
                        if range70:
                            num = float(str[4].split(",")[1])
                            self.range70.append(num)
                    matchObj = re.match(r'Velocity Test *', line, re.M | re.I)
                    if matchObj:
                        str = line.split(" ")
                        vlcN10 = re.match(r'-10m/s*', str[3], 0)
                        if vlcN10:
                            num = float(str[4].split(",")[1])
                            self.vlcN10.append(num)
                        vlcN5 = re.match(r'-5m/s*', str[3], 0)
                        if vlcN5:
                            num = float(str[4].split(",")[1])
                            self.vlcN5.append(num)
                        vlc5 = re.match(r'5m/s*', str[3], 0)
                        if vlc5:
                            num = float(str[4].split(",")[1])
                            self.vlc5.append(num)
                        vlc10 = re.match(r'10m/s*', str[3], 0)
                        if vlc10:
                            num = float(str[4].split(",")[1])
                            self.vlc10.append(num)
        print(counter)
        print(self.angle3)

    def calcCharac(self):
        meanN7, varN7 = self.calcVariance(self.angleN7)
        meanN5, varN5 = self.calcVariance(self.angleN5)
        meanN3, varN3 = self.calcVariance(self.angleN3)
        mean3, var3 = self.calcVariance(self.angle3)
        mean5, var5 = self.calcVariance(self.angle5)
        mean7, var7 = self.calcVariance(self.angle7)
        report = "测角，目标值-7度，实测均值：" + str(meanN7) + ", 方差：" + str(varN7) + '\n'
        self.writeReport(report)
        report = "测角，目标值-5度，实测均值：" + str(meanN5) + ", 方差：" + str(varN5) + '\n'
        self.writeReport(report)
        report = "测角，目标值-3度，实测均值：" + str(meanN3) + ", 方差：" + str(varN3) + '\n'
        self.writeReport(report)
        report = "测角，目标值3度，实测均值：" + str(mean3) + ", 方差：" + str(var3) + '\n'
        self.writeReport(report)
        report = "测角，目标值5度，实测均值：" + str(mean5) + ", 方差：" + str(var5) + '\n'
        self.writeReport(report)
        report = "测角，目标值7度，实测均值：" + str(mean7) + ", 方差：" + str(var7) + '\n'
        self.writeReport(report)
        #print("测角，目标值-7度，实测均值：", meanN7, ", 方差：", varN7)
        #print("测角，目标值-5度，实测均值：", meanN5, ", 方差：", varN5)
        #print("测角，目标值-3度，实测均值：", meanN3, ", 方差：", varN3)
        #print("测角，目标值3度，实测均值：", mean3, ", 方差：", var3)
        #print("测角，目标值5度，实测均值：", mean5, ", 方差：", var5)
        #print("测角，目标值7度，实测均值：", mean7, ", 方差：", var7)
        meanR10, varR10 = self.calcVariance(self.range10)
        meanR20, varR20 = self.calcVariance(self.range20)
        meanR30, varR30 = self.calcVariance(self.range30)
        meanR40, varR40 = self.calcVariance(self.range40)
        meanR50, varR50 = self.calcVariance(self.range50)
        meanR60, varR60 = self.calcVariance(self.range60)
        meanR70, varR70 = self.calcVariance(self.range70)
        report = "测距，目标值10m，实测均值：" + str(meanR10) + ", 方差：" + str(varR10)+ '\n'
        self.writeReport(report)
        report = "测距，目标值20m，实测均值：" + str(meanR20) + ", 方差：" + str(varR20)+ '\n'
        self.writeReport(report)
        report = "测距，目标值30m，实测均值：" + str(meanR30) + ", 方差：" + str(varR30)+ '\n'
        self.writeReport(report)
        report = "测距，目标值40m，实测均值：" + str(meanR40) + ", 方差：" + str(varR40)+ '\n'
        self.writeReport(report)
        report = "测距，目标值50m，实测均值：" + str(meanR50) + ", 方差：" + str(varR50)+ '\n'
        self.writeReport(report)
        report = "测距，目标值60m，实测均值：" + str(meanR60) + ", 方差：" + str(varR60)+ '\n'
        self.writeReport(report)
        report = "测距，目标值70m，实测均值：" + str(meanR70) + ", 方差：" + str(varR70)+ '\n'
        self.writeReport(report)
        #print("测距，目标值10m，实测均值：", meanR10, "方差：", varR10)
        #print("测距，目标值20m，实测均值：", meanR20, "方差：", varR20)
        #print("测距，目标值30m，实测均值：", meanR30, "方差：", varR30)
        #print("测距，目标值40m，实测均值：", meanR40, "方差：", varR40)
        #print("测距，目标值50m，实测均值：", meanR50, "方差：", varR50)
        #print("测距，目标值60m，实测均值：", meanR60, "方差：", varR60)
        #print("测距，目标值70m，实测均值：", meanR70, "方差：", varR70)
        meanVN10, varVN10 = self.calcVariance(self.vlcN10)
        meanVN5, varVN5 = self.calcVariance(self.vlcN5)
        meanV5, varV5 = self.calcVariance(self.vlc5)
        meanV10, varV10 = self.calcVariance(self.vlc10)
        report = "测速，目标值-10m/s，实测均值：" + str(meanVN10) + ", 方差：" + str(varVN10)+ '\n'
        self.writeReport(report)
        report = "测速，目标值-5m/s，实测均值：" + str(meanVN5) + ", 方差：" + str(varVN5)+ '\n'
        self.writeReport(report)
        report = "测速，目标值5m/s，实测均值：" + str(meanV5) + ", 方差：" + str(varV5)+ '\n'
        self.writeReport(report)
        report = "测速，目标值10m/s，实测均值：" + str(meanV10) + ", 方差：" + str(varV10)+ '\n'
        self.writeReport(report)
        #print("测速，目标值-10m/s，实测均值：", meanVN10, ", 方差：", varVN10)
        #print("测速，目标值-5m/s，实测均值：", meanVN5, ", 方差：", varVN5)
        #print("测速，目标值5m/s，实测均值：", meanV5, ", 方差：", varV5)
        '''
        plt.figure(1)
        plt.title("difference value with velocity -10m/s")
        plt.ylabel("counters")
        data = [i + 10 for i in self.vlcN10]
        plt.hist(data, bins=np.arange(-1,12,0.2))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(2)
        plt.title("difference value with velocity -5m/s")
        plt.ylabel("counters")
        data = [i + 5 for i in self.vlcN5]
        plt.hist(data, bins=np.arange(-6,6,0.2))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(3)
        plt.title("difference value with velocity 5m/s")
        plt.ylabel("counters")
        data = [i - 5 for i in self.vlc5]
        plt.hist(data, bins=np.arange(-6, 6, 0.2))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(4)
        plt.title("difference value with velocity 10m/s")
        plt.ylabel("counters")
        data = [i - 10 for i in self.vlc10]
        plt.hist(data, bins=np.arange(-11, 1, 0.2))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(5)
        plt.title("difference value with Range 10")
        plt.ylabel("counters")
        data = [i - 10 for i in self.range10]
        plt.hist(data, bins=np.arange(-11, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(6)
        plt.title("difference value with Range 20")
        plt.ylabel("counters")
        data = [i - 20 for i in self.range20]
        plt.hist(data, bins=np.arange(-21, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(7)
        plt.title("difference value with Range 30")
        plt.ylabel("counters")
        data = [i - 30 for i in self.range30]
        plt.hist(data, bins=np.arange(-31, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(8)
        plt.title("difference value with Range 40")
        plt.ylabel("counters")
        data = [i - 40 for i in self.range40]
        plt.hist(data, bins=np.arange(-41, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(9)
        plt.title("difference value with Range 50")
        plt.ylabel("counters")
        data = [i - 50 for i in self.range50]
        plt.hist(data, bins=np.arange(-51, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(10)
        plt.title("difference value with Range 60")
        plt.ylabel("counters")
        data = [i - 60 for i in self.range60]
        plt.hist(data, bins=np.arange(-61, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(10)
        plt.title("difference value with Range 70")
        plt.ylabel("counters")
        data = [i - 70 for i in self.range70]
        plt.hist(data, bins=np.arange(-71, 1, 0.6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()
        '''
        plt.figure(11)
        plt.title("difference value with Angle -7°")
        #plt.xlim(-8.0, -5)
        plt.ylabel("counters")
        data = [i + 7 for i in self.angleN7]
        plt.hist(data, bins=np.arange(-1, 8, 0.1))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(12)
        plt.title("difference value with Angle -5°")
        plt.ylabel("counters")
        data = [i + 5 for i in self.angleN5]
        plt.hist(data, bins=np.arange(-1, 4, 0.1))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()


        plt.figure(13)
        plt.title("difference value with Angle -3°")
        plt.ylabel("counters")
        data = [i + 3 for i in self.angleN3]
        plt.hist(data, bins=np.arange(-1, 3, 0.1))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(14)
        plt.title("difference value with Angle 3°")
        plt.ylabel("counters")
        data = [i - 3 for i in self.angle3]
        plt.hist(data, bins=np.arange(-3, 3, 0.1))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(15)
        plt.title("difference value with Angle 5°")
        plt.ylabel("counters")
        data = [i - 5 for i in self.angle5]
        plt.hist(data, bins=np.arange(-4, 4, 0.1))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

        plt.figure(16)
        plt.title("difference value with Angle 7°")
        plt.ylabel("counters")
        data = [i - 7 for i in self.angle7]
        plt.hist(data, bins=np.arange(-4, 4, 0.1))
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

    def calcVariance(self, ls):
        N7 = []
        for fl in ls:
            if fl != 0.0:
                N7.append(fl)
        mean = np.mean(N7,dtype=np.float32)
        var = np.var(N7)
        return mean, var

    def getFileName(self):
        fileList = []
        file_dir = os.getcwd()
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                # print(file)
                if os.path.splitext(file)[1] == '.csv':  # os.path.splitext()函数将路径拆分为文件名+扩展名
                    # if file.split('.')[1].strip() == 'txt':
                    fileList.append(os.path.join(root, file))
        return fileList

rdcsv = rdCsv()
rdcsv.rdCsv()
rdcsv.calcCharac()
#print("matplot file location",matplotlib.matplotlib_fname())

