import sys
import os
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from data_sorter import data_read, data_search

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setGeometry(50, 50, 400, 450)
        self.setFixedSize(400, 70+(50*len(data_list)))

        self.setWindowTitle("Search Window")

        section1 = QVBoxLayout()

        self.checkBtns = [0] * len(data_list)
        for i in range(len(data_list)):
            self.checkBtns[i] = QCheckBox(os.path.basename(data_list[i]))
            self.checkBtns[i].toggle()
            section1.addWidget(self.checkBtns[i])

        self.label = QLabel('Please input "," separated pattern.')
        self.textFolder = QLineEdit()
        self.searchBtn = QPushButton('search!')
        self.searchBtn.clicked.connect(self.startSearch)

        section1.addWidget(self.label)
        section1.addWidget(self.textFolder)
        section1.addWidget(self.searchBtn)

        self.setLayout(section1)

    def startSearch(self):
        data_copy = data_list.copy()
        for data_index in range(len(data_copy)):
            if self.checkBtns[data_index].isChecked() == False:
                data_copy[data_index] = 0
        data_copy = [i for i in data_copy if i != 0]

        input_keyword = self.textFolder.text()
        output_data_list = data_search(data_copy, input_keyword)

        if len(output_data_list) == 0:
            self.alert = QMessageBox.information(self, 'No result', 'The result does not exit!')
        else:
            subWindow = SubWindow(self)
            subWindow.show()

class SubWindow:
    def __init__(self, parent=None):
        self.w = QDialog(parent)
        self.w.setGeometry(100, 100, 400, 450)
        self.w.setFixedSize(800, 500)
        self.w.setWindowTitle("Table Window")
        self.parent = parent

        data_copy = data_list.copy()
        for data_index in range(len(data_copy)):
            if self.parent.checkBtns[data_index].isChecked() == False:
                data_copy[data_index] = 0
        data_copy = [i for i in data_copy if i != 0]

        input_keyword = self.parent.textFolder.text()
        output_data_list = data_search(data_copy, input_keyword)
        self.data = output_data_list
        self.input_data = list(output_data_list.values())[0]

        self.tableView = QTableView()
        self.tableView.clicked.connect(self.viewClicked)

        self.tableView.setStyleSheet("QTableView{gridline-color: black}")

        self.model = TableModel(self.input_data)
        self.tableView.setModel(self.model)


        section2 = QVBoxLayout()

        div1 = QHBoxLayout()
        self.checked = ''
        self.dataBtns = [0] * len(output_data_list)
        for m in range(len(output_data_list)):
            self.dataBtns[m] = QRadioButton(list(output_data_list.keys())[m])
            self.dataBtns[m].toggled.connect(self.changeData)
            div1.addWidget(self.dataBtns[m])
        self.dataBtns[0].setChecked(True)

        div2 = QHBoxLayout()
        self.saveBtn = QPushButton('Save')
        self.saveBtn.clicked.connect(self.handleSave)
        div2.addWidget(self.saveBtn)

        section2.addWidget(self.tableView)
        section2.addLayout(div1)
        section2.addLayout(div2)
        self.w.setLayout(section2)

    def viewClicked(self, indexClicked):
        print('indexClicked() row: %s  column: %s'%(indexClicked.row(), indexClicked.column() ))
        self.selectRow = indexClicked.row()

    def handleSave(self):
        df = pd.DataFrame(self.input_data)
        df = df.reset_index(drop=True)
        df.to_csv('results/result_'+str(self.checked)+'.csv')


    def changeData(self):
        radioBtn = self.parent.sender()
        self.checked = radioBtn.text()
        if radioBtn.isChecked() == True:
            self.input_data = self.data[self.checked]
            self.model = TableModel(self.input_data)
            self.tableView.setModel(self.model)

    def show(self):
        self.w.exec_()

class TableModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    data_list = data_read()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
