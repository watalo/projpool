#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__:"watalo"
# @Time: 2020/3/14 22:25
# @Site    : 
# @File    : call_uipp.py
# @Software: PyCharm

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tinydb import Query
from uipp import Ui_MainWindow
from proj_input import Ui_Dialog
from core import Product, Project, ProjPool

class pp_main_win(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(pp_main_win, self).__init__(parent)
        self.setupUi(self)
        self.btn_addproj.clicked.connect(self.add_proj)
        self.ProjPool_obj = ProjPool()
        self.proj_show_in_table()



    def proj_show_in_table(self):  #将数据库中的数据现实在tableView中
        table_proj = self.ProjPool_obj.db.table('proj')
        header_label_list = ['企业名称','客户经理','营销状态','授信额度','可用额度','已用额度','用信笔数']
        len_row = len(table_proj)
        self.model = QStandardItemModel(len_row,7)
        self.model.setHorizontalHeaderLabels(header_label_list)
        self.tableView_proj.setModel(self.model)
        for proj in table_proj:
            for header_label in header_label_list:
                item = QStandardItem(str(proj[header_label]))
                self.model.setItem(proj.doc_id-1,
                                   header_label_list.index(header_label),
                                   item)



    def add_proj(self):
        dialog = proj_input_dialog(self)
        dialog.show()


class proj_input_dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(proj_input_dialog, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.proj_save)
        self.name = ''
        self.credit_amount = int()
        self.manager = ''

    def proj_save(self):
        self.name = self.lineEdit.text()
        self.manager = self.lineEdit_2.text()
        self.credit_amount = int(self.lineEdit_3.text())
        proj =  Project(name=self.name,
                        credit_amount=self.credit_amount,
                        manager=self.manager)
        win.ProjPool_obj.add_project(proj)
        win.proj_show_in_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = pp_main_win()
    win.show()
    app.exit(app.exec_())