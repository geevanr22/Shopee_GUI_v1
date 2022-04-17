from PyQt5.QtWidgets import (QTabWidget, QApplication,
                             QVBoxLayout, QDialog)

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import sys
import os
from ja1_tab1CompanyBrief import Tab1
from ja1_tab2_Outputs import Tab2

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AS & Associates ARK Database System')
        self.setGeometry(200, 0, 800, 600)
        flag = Qt.WindowMinMaxButtonsHint
        self.setWindowFlag(flag)


        # Add Tabs to TabWidget
        self.vbox = QVBoxLayout()
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(Tab1(), 'Company Brief')
        self.tabWidget.addTab(Tab2(), 'Saved Records')


        self.vbox.addWidget(self.tabWidget)
        self.setLayout(self.vbox)

        # Generate Scanned Folder at start of the programme
        cwd = os.getcwd()  # Get current working directory to be used below

        scanned_documents = 'Scanned_Documents'
        if not os.path.isdir(f'{cwd}\\{scanned_documents}'):  # check if Scan Folder exists
            print('Scanned Docs Folder does not exists')
            os.mkdir(scanned_documents) # if scan docs folder does not exist create one
        if os.path.isdir(f'{cwd}\\{scanned_documents}'):
            print('Scanned Docs has already been Generated') # else do nothing



# global app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
