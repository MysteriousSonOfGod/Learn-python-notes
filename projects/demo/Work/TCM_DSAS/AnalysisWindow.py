#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    21:18  2019/12/12
#@Author  :    tb_youth
#@FileName:    PlotOnWindow.py
#@SoftWare:    PyCharm
#@Blog    :    http://blog.csdn.net/tb_youth

'''
在窗口中使用matlibplot绘制图形
'''
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout,QWidget
from PyQt5.QtWidgets import QTableView,QHBoxLayout,QFileDialog
from PyQt5.QtGui import QStandardItem,QStandardItemModel,QColor
import matplotlib.pyplot as plt
import sys
import random
import datetime
from openpyxl import workbook

from projects.demo.Work.TCM_DSAS.DataFrameListMTF import DataFrameListMTF as DTL


class AnalysisWindowDemo(QWidget):
    def __init__(self):
        super(AnalysisWindowDemo,self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('分析预测')
        #需要的数据
        self.RMSE = None
        self.y_predict = None
        self.plt = plt

        # 创建一个展示板
        self.figure = self.plt.figure(facecolor='#66CCFF')
        self.canvas = FigureCanvas(self.figure)
        self.predict_button = QPushButton('预测')
        self.draw_button = QPushButton('绘图')
        self.output_button = QPushButton('导出')
        # self.input_button = QPushButton('导入')
        # 显示用于分析的数据
        self.table_view = QTableView()
        self.table_view.setModel(QStandardItemModel(100, 100))

        # 设置布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.table_view)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.predict_button)
        vlayout.addWidget(self.draw_button)
        vlayout.addWidget(self.output_button)
        # vlayout.addWidget(self.input_button)
        vlayout.addStretch()
        vlayout.setSpacing(10)
        hlayout.addItem(vlayout)
        layout = QVBoxLayout()
        layout.addItem(hlayout)
        layout.addWidget(self.canvas)
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        # 绑定信号
        self.draw_button.clicked.connect(self.onClickDraw)
        self.predict_button.clicked.connect(self.onClickPredict)
        self.output_button.clicked.connect(self.onClickOutput)

    def onClickPredict(self):
        if self.y_predict is None:
            return
        self.predict_button.setEnabled(False)
        self.model = QStandardItemModel()
        dtl = DTL()
        data_list = dtl.DataFrame_to_list(self.y_predict)
        for rows in data_list:
            row = [QStandardItem(str(cell)) for cell in rows]
            self.model.appendRow(row)
        RMSE = ['old_RMSE:', self.RMSE[0], 'now_RMSE:', self.RMSE[1]]
        row = [QStandardItem(str(cell)) for cell in RMSE]
        #突出显示RMSE
        row[1].setBackground(QColor(0, 255, 0))
        row[1].setForeground(QColor(255, 0, 0))
        row[-1].setBackground(QColor(0, 255, 0))
        row[-1].setForeground(QColor(255, 0, 0))
        self.model.appendRow(row)
        self.table_view.setModel(self.model)


    def onClickDraw(self):
        if self.y_predict is  None:
            return
        self.plt = plt
        #这里开始就按照matlibplot的方式绘图
        try:
            # 中文乱码处理
            self.plt.rcParams['font.sans-serif'] = ['SimHei']
            self.plt.rcParams['axes.unicode_minus'] = False

            #数据
            index = random.sample(self.y_predict.index.tolist(), 10)
            y_list = self.y_predict['y'].tolist()
            data = [item for i, item in enumerate(y_list) if i in index]

            y_old_predict_list = self.y_predict['y'].tolist()
            data1 = [item for i, item in enumerate(y_old_predict_list) if i in index]

            y_now_predict_list = self.y_predict['y'].tolist()
            data2 = [item for i, item in enumerate(y_now_predict_list) if i in index]


            index.sort()
            x = [str(i) for i in index]


            # self.plt.plot(x, data, marker='.', mec='g', label='y')
            self.plt.plot(x, data1, marker='o', mec='b', label='y_old_predict')
            self.plt.plot(x, data2, marker='*', mec='r', label='y_now_predict')

            # label显示
            self.plt.legend()

            # x轴数值标记,这个一定要在后面加上
            self.plt.xticks(x)

           #确定y轴数值范围
            minx = min(min(y_old_predict_list), min(y_now_predict_list))
            maxx = max(max(y_now_predict_list), max(y_old_predict_list))
            self.plt.ylim(minx - 100, maxx + 500)

            # # 标上数值
            # for x, y in enumerate(data1):
            #     plt.text(x, y + 100, '%s' % y, ha='center')
            #
            # for x, y in enumerate(data2):
            #     plt.text(x, y + 500, '%s' % y, ha='center')

            # 设置标题
            self.plt.title("预测结果对比")


            # 按照matlibplot的方式绘制之后，在窗口上绘制
            self.canvas.draw()
        except Exception as e:
            print(e)

        self.draw_button.setEnabled(False)

    def onClickOutput(self):
        if self.y_predict is None:
            return
        #输出表格中结果
        file_path, self.save = QFileDialog.getSaveFileName(self, '保存文件', './result',
                                                           'ALL Files(*);;xlsx(*.xlsx);;xls(*.xls);;csv(*.csv)')
        wb = workbook.Workbook()
        wb.encoding='utf-8'
        wa = wb.active
        # 文件中写入数据
        try:
            rows = self.model.rowCount()
            columns = self.model.columnCount()
            for i in range(rows):
                item = []
                for j in range(columns):
                    item.append(self.model.index(i, j).data())
                wa.append(item)
            wb.save(file_path)
        except Exception as e:
            print(e)
        try:
            nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.plt.savefig('./result/res1.svg')
        except:
            pass






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = AnalysisWindowDemo()
    main_window.show()
    app.exec()


