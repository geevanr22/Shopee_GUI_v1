import sys
import sqlite3
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QStackedWidget, QVBoxLayout, QHBoxLayout,)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ja1_filingEngine import FilingSystem


class StackedFilingSystem(QWidget):
    def __init__(self):
        super().__init__()

        #Set Window Title

        self.setWindowTitle('Filing Tray')
        self.setGeometry(1530,580,400,300)
        self.show()

        # StackedWidget
        self.stackedWidget = QStackedWidget()
        self.docFolderNameList = ['Directors_Circular', 'Members_Meeting']

        # this gives you the number of folder names in the list
        self.countDocFolderNameList = len(self.docFolderNameList)


        for self.folder in self.docFolderNameList:

            self.stackedWidget.addWidget(FilingSystem(f"{self.folder}"))
            # self.stackedWidget.addWidget(FilingSystem(f"{self.folder.replace('_',' ')}"))


        self.stackedWidgetButtons()
        self.layoutSetup()


    def stackedWidgetButtons(self):
        # Note: StackedWidget Buttons (Separate from the filing system buttons, StackedWidget Buttons are fixed to the StackedWidget)
        self.prevButton = QPushButton('Previous')
        self.prevButton.clicked.connect(self.clickPreviousButton)
        self.nextButton = QPushButton('Next')
        self.nextButton.clicked.connect(self.clickNextButton)

    def clickPreviousButton(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex()-1) % int(f'{self.countDocFolderNameList}')) # programatically fetches the number of folders in list

    def clickNextButton(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex()+1) % int(f'{self.countDocFolderNameList}')) # programatically fetches the number of folders in list

    def layoutSetup(self):

        #Button Layout
        self.buttonLayout_h = QHBoxLayout()
        self.buttonLayout_h.addWidget(self.prevButton)
        self.buttonLayout_h.addWidget(self.nextButton)

        #MainLayouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addSpacing(10)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.stackedWidget)
        self.mainLayout.addLayout(self.buttonLayout_h)
        self.setLayout(self.mainLayout)



# app = QApplication(sys.argv)
# window = StackedFilingSystem()
# sys.exit(app.exec())
