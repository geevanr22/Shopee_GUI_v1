# Functions for Tab1 Form
# These functions sets up the database and adds the inputs to the DB
# This module will then be imported from the main.py file
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QAbstractScrollArea, QTableWidget,
                             QTableWidgetItem, QLabel, QLineEdit, QHBoxLayout)
import sys
import sqlite3
from ja1_deepViewUpdateWindow import DeepViewUpdateWindow
from custom_message_box import custom_message


class Tab2(QWidget):
    def __init__(self):
        super().__init__()

        # Display Records from the Database
        # Search Function
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.table.setRowCount(5)
        self.table.setColumnCount(10)

        self.table.setHorizontalHeaderLabels(['File No', 'Company Name', 'Co Old Name', 'Reg No', 'Date of Change', 'Inc Date', 'Co Type',
        'Co Status', 'Directors Circular', 'Members Meeting'])

        self.refreshRecordsBtn = QPushButton('Refresh Records')
        self.refreshRecordsBtn.clicked.connect(self.loadData)
        # self.showRecordBtn = QPushButton("Quick View")
        # self.showRecordBtn.clicked.connect(self.getRowForQuickView)
        self.deepViewUpdateBtn = QPushButton('Deep View')
        self.deepViewUpdateBtn.clicked.connect(self.deepViewWithBriefLayout)

        self.mainLayoutTab2 = QVBoxLayout()
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.table)
        # self.tableLayout.addSpacing(50)

        self.buttonHLayout = QHBoxLayout()
        self.buttonHLayout.addWidget(self.refreshRecordsBtn)
        # self.buttonHLayout.addWidget(self.showRecordBtn)
        self.buttonHLayout.addWidget(self.deepViewUpdateBtn)
        self.mainLayoutTab2.addLayout(self.tableLayout)
        self.mainLayoutTab2.addLayout(self.buttonHLayout)

        self.setLayout(self.mainLayoutTab2)
        self.loadData()

    def deepViewWithBriefLayout(self):

        try:
            self.getRowForDeepView()

            selectedRowToDeepView = [self.field1,
                                     self.field2,
                                     self.field3,
                                     self.field4,
                                     self.field5,
                                     self.field6,
                                     self.field7,
                                     self.field8]

            selectedRow =  self.selectedRow
            self.window2 = DeepViewUpdateWindow(selectedRowToDeepView)
            self.window2.show()
        except:
            pass

    def loadData(self):
        self.con = sqlite3.connect("ja1.db")
        self.cur = self.con.cursor()
        self.query = "SELECT * FROM JA1"
        self.cur.execute(self.query)

        self.table.setRowCount(10)
        tableRowIndex = 0
        for row in self.cur.execute(self.query):
            self.table.setItem(tableRowIndex, 0, QTableWidgetItem(row[0]))
            self.table.setItem(tableRowIndex, 1, QTableWidgetItem(row[1]))
            self.table.setItem(tableRowIndex, 2, QTableWidgetItem(row[2]))
            self.table.setItem(tableRowIndex, 3, QTableWidgetItem(row[3]))
            self.table.setItem(tableRowIndex, 4, QTableWidgetItem(row[4]))
            self.table.setItem(tableRowIndex, 5, QTableWidgetItem(row[5]))
            self.table.setItem(tableRowIndex, 6, QTableWidgetItem(row[6]))
            self.table.setItem(tableRowIndex, 7, QTableWidgetItem(row[7]))
            # self.table.setItem(tableRowIndex, 8, QTableWidgetItem(row[8]))
            # self.table.setItem(tableRowIndex, 9, QTableWidgetItem(row[9]))
            #

            tableRowIndex += 1

    def getRowForQuickView(self):

        tab2 = Tab2()
        tab2.show()

        try:

            self.selectedRow = self.table.currentRow()

            self.field1 = self.table.item(self.selectedRow, 0).text()
            self.field2 = self.table.item(self.selectedRow, 1).text()
            self.field3 = self.table.item(self.selectedRow, 2).text()
            self.field4 = self.table.item(self.selectedRow, 3).text()
            self.field5 = self.table.item(self.selectedRow, 4).text()
            self.field6 = self.table.item(self.selectedRow, 5).text()
            self.field7 = self.table.item(self.selectedRow, 6).text()
            self.field8 = self.table.item(self.selectedRow, 7).text()



            self.displaySelectedRecords()

        except:
            custom_message('Please select a record to be displayed')


    def getRowForDeepView(self):

        try:
            self.selectedRow = self.table.currentRow()

            self.field1 = self.table.item(self.selectedRow, 0).text()
            self.field2 = self.table.item(self.selectedRow, 1).text()
            self.field3 = self.table.item(self.selectedRow, 2).text()
            self.field4 = self.table.item(self.selectedRow, 3).text()
            self.field5 = self.table.item(self.selectedRow, 4).text()
            self.field6 = self.table.item(self.selectedRow, 5).text()
            self.field7 = self.table.item(self.selectedRow, 6).text()
            self.field8 = self.table.item(self.selectedRow, 7).text()



        except:
            custom_message('Please select a record to be displayed')

    def displaySelectedRecords(self):
        """Layout, labels and lineEdits that displays the table selection"""
        # Main Vertical Box Layout for Output Section



        self.mainQuickViewVboxLayout = QVBoxLayout()




        # Horizontal Line 1
        self.hboxLayoutLine1 = QHBoxLayout() #-------------------------------------------- Hrizontal Layout 1

        # File No
        self.fileNoLabel = QLabel('File No:')
        self.fileNoOutputLabel = QLabel(f'{self.field1}')

        # Company Name
        self.coNameLabel = QLabel('Company Name:')
        self.coNameOutputLabel = QLabel(f'{self.field2}')

        # Company Reg No
        self.coRegNoLabel = QLabel('Reg No:')
        self.coRegNoOutputLabel = QLabel(f'{self.field4}')

        # Company Old Name
        self.coOldNameLabel = QLabel('Company Old Name:')
        self.coOldNameOutputLabel = QLabel(f'{self.field3}')

        # Add Widgets to Horizontal Layout 1
        self.hboxLayoutLine1.addWidget(self.fileNoLabel)
        self.hboxLayoutLine1.addWidget(self.fileNoOutputLabel)
        self.hboxLayoutLine1.addWidget(self.coNameLabel)
        self.hboxLayoutLine1.addWidget(self.coNameOutputLabel)
        self.hboxLayoutLine1.addWidget(self.coRegNoLabel)
        self.hboxLayoutLine1.addWidget(self.coRegNoOutputLabel)
        self.hboxLayoutLine1.addWidget(self.coOldNameLabel)
        self.hboxLayoutLine1.addWidget(self.coOldNameOutputLabel)
        #----------------------------------------------------------------------------------------------------

        self.hboxLayoutLine2 = QHBoxLayout() #-------------------------------------------- Hrizontal Layout 2

        # Date of Change
        self.dateOfChangeLabel = QLabel('Name Changed:')
        self.dateOfChangeOutputLabel = QLabel(f'{self.field5}')

        # Incorporated Date
        self.incorporatedDateLabel = QLabel('Inc:')
        self.incorporatedDateOutputLabel = QLabel(f'{self.field6}')

        # Company Type
        self.companyTypeLabel = QLabel('Type:')
        self.companyTypeOutputLabel = QLabel(f'{self.field7}')

        # Company Status
        self.companyStatusLabel = QLabel('Status:')
        self.companyStatusOutputLabel = QLabel(f'{self.field8}')

        # Add Widgets to Horizontal Layout 2
        self.hboxLayoutLine2.addWidget(self.dateOfChangeLabel)
        self.hboxLayoutLine2.addWidget(self.dateOfChangeOutputLabel)
        self.hboxLayoutLine2.addWidget(self.incorporatedDateLabel)
        self.hboxLayoutLine2.addWidget(self.incorporatedDateOutputLabel)
        self.hboxLayoutLine2.addWidget(self.companyTypeLabel)
        self.hboxLayoutLine2.addWidget(self.companyTypeOutputLabel)
        self.hboxLayoutLine2.addWidget(self.companyStatusLabel)
        self.hboxLayoutLine2.addWidget(self.companyStatusOutputLabel)


        # Add HBox Text Layouts (Horizontal Lines) Layouts to main/QuickView Section's VBox layout
        self.mainQuickViewVboxLayout.addLayout(self.hboxLayoutLine1)
        self.mainQuickViewVboxLayout.addLayout(self.hboxLayoutLine2)


        # Vertical spacing between show record button and the bottom of widget
        self.mainQuickViewVboxLayout.addSpacing(20)

        # Add VBox to Main Layout
        self.mainLayoutTab2.addLayout(self.mainQuickViewVboxLayout)





        # print(self.mainQuickViewVboxLayout)
        # # self.mainQuickViewVboxLayout


