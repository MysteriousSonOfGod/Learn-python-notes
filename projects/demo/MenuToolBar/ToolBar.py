#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2019/10/22 0022 9:46
#@Author  :    tb_youth
#@FileName:    ToolBar.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

from PyQt5.QtWidgets import QApplication,QMainWindow,QToolBar,QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import os


class ToolBarDemo(QMainWindow):
    def __init__(self,parent=None):
        super(ToolBarDemo,self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(800,800)
        self.setWindowTitle('ToolBarDemo')
        self.setWindowIcon(QIcon('D:\Learn-python-notes\projects\demo\icon\分析.png'))

        #工具栏
        toolbar1 = self.addToolBar('File')
        new = QAction(QIcon('D:\Learn-python-notes\projects\demo\icon\新建.png'),'new',self)
        toolbar1.addAction(new)

        open = QAction(QIcon('D:\Learn-python-notes\projects\demo\icon\打开.png'),'open',self)
        toolbar1.addAction(open)

        save = QAction(QIcon('D:\Learn-python-notes\projects\demo\icon\保存.png'),'save',self)
        toolbar1.addAction(save)

        toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar2 = self.addToolBar('Setting')
        setting = QAction(QIcon('D:\Learn-python-notes\projects\demo\icon\设置.png'),'setting',self)
        toolbar2.addAction(setting)
        toolbar2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        toolbar1.actionTriggered.connect(self.toolbtnPressed)
        toolbar2.actionTriggered.connect(self.toolbtnPressed)

    def toolbtnPressed(self,a):
        #print('%s被按下'%a.text())
        if a.text() == 'open':
            os.system('start explorer D:\Learn-python-notes\material\科研实践\数据')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToolBarDemo()
    window.show()
    sys.exit(app.exec_())


