from PyQt5.QtWidgets import (QTabWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QDateEdit, QTextEdit,
                             QVBoxLayout, QDialog, QWidget, QLineEdit, QRadioButton, QWidget, QButtonGroup,
                             QScrollArea, QComboBox)

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtCore
from custom_message_box import custom_message

import sys
import os
import sqlite3




class DeepViewUpdateWindow(QWidget): # Name here has been changed to MainWindow2
    def __init__(self, selectedRowToDeepView):
        super().__init__()


        self.setWindowTitle('JA1_DeepView')
        self.setGeometry(700, 70, 1130, 900)
        self.setMaximumWidth(1130)
        flag = Qt.WindowMinMaxButtonsHint
        self.setWindowFlag(flag)

        # Database
        self.databaseName = 'JA1'
        self.databaseName = f'{self.databaseName}.db'
        self.tableName = 'ja1'

        self.selectedRow1 = selectedRowToDeepView
        self.comboBoxCompanyList()



        self.uiSetup3()



    def uiSetup3(self):
        # File No

        # ComboBox Layout for Company Selection in DeepView Mode
        self.comboBoxLabel = QLabel('Select company to edit')
        self.comboHBoxLayout = QHBoxLayout()
        self.comboVBoxLayout = QVBoxLayout()
        self.comboBoxDeepView = QComboBox()
        self.comboBoxDeepView.addItems(self.comboBoxList)
        self.ifComboBoxItemSelected() # This signals when combobox item has been selected


        self.comboBoxDeepView.setMaximumWidth(200)
        self.comboVBoxLayout.addWidget(self.comboBoxLabel)
        self.comboVBoxLayout.addWidget(self.comboBoxDeepView)
        self.comboHBoxLayout.addLayout(self.comboVBoxLayout)


        # Horizontal Layout 1

        self.horizontalLayout_1 = QHBoxLayout()
        self.label_fileNo = QLabel('File No')
        self.horizontalLayout_1.addWidget(self.label_fileNo)
        self.lineEdit_3_FileNo = QLineEdit()

        # File NO Input
        self.lineEdit_3_FileNo.setText(self.selectedRow1[0]) #<-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_3_FileNo)

        self.label_name = QLabel('Company Name')
        self.horizontalLayout_1.addWidget(self.label_name)
        self.lineEdit_coName = QLineEdit()
        self.lineEdit_coName.setText(self.selectedRow1[1])        #<-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_coName)

        self.label_oldName = QLabel('Old Name')
        self.horizontalLayout_1.addWidget(self.label_oldName)
        self.lineEdit_coOldName = QLineEdit()
        self.lineEdit_coOldName.setText(self.selectedRow1[2])     #<-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_coOldName)

        self.label_regNo = QLabel('Reg No')
        self.horizontalLayout_1.addWidget(self.label_regNo)
        self.lineEdit_regNo = QLineEdit()
        self.lineEdit_regNo.setText(self.selectedRow1[3])         #<-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_regNo)

        # Horizontal Line 2 Date of Change ############################################################################################################
        self.label_DateOfChange = QLabel('Date Of Change')

        self.newDateEditDateOfChange = self.selectedRow1[4] #<-------------------------------------------
        self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")

        self.dateEditDateOfChange = QDateEdit()
        self.dateEditDateOfChange.setDisplayFormat("d-MMM-yyyy")
        self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)




        # https://www.geeksforgeeks.org/pyqt5-qdateedit-date-changed-signal/
        # Need to check if date is changed and if not need to put out a message or else set date to something obvious as unusable
        


        # Horizontal Line 2 : Date Incorporated
        self.label_IncorporatedDate = QLabel('Incorporated Date')

        self.newDateEditIncorporatedDate = self.selectedRow1[5]
        self.setDateNewDateEditIncorporatedDateString = QDate.fromString(self.newDateEditIncorporatedDate, "d-MMM-yyyy")

        self.dateEditIncorporatedDate = QDateEdit()
        self.dateEditIncorporatedDate.setDisplayFormat("d-MMM-yyyy") #<-------------------------------------------------------- Date Incorporated
        self.dateEditIncorporatedDate.setDate(self.setDateNewDateEditIncorporatedDateString)


        # Vertical Layout for Date of Change and Incorporation
        self.dateOfChangeVerticalLayout_1 = QVBoxLayout()
        self.dateOfChangeVerticalLayout_1.addWidget(self.label_DateOfChange)
        self.dateOfChangeVerticalLayout_1.addWidget(self.dateEditDateOfChange)

        self.dateOfIncorporationVerticalLayout_1 = QVBoxLayout()
        self.dateOfIncorporationVerticalLayout_1.addWidget(self.label_IncorporatedDate)
        self.dateOfIncorporationVerticalLayout_1.addWidget(self.dateEditIncorporatedDate)


        # Vertical Layout: Type of Company
        self.radioButtonTypeVerticalLayout_1 = QVBoxLayout()
        self.typeLabel = QLabel('Type')
        self.typeLabelBlank = QLabel('')  # This is used to insert blank spacing
        #--------------------------------------------------------------------------------------Radio Buttons--------------------
        # Radio Buttons: Type of Company

        self.typeRadioButton_1 = QRadioButton('Limited By Shares')
        self.typeRadioButton_2 = QRadioButton('Private Limited')

        if self.selectedRow1[6] == 'Limited By Shares':
            self.typeRadioButton_1.setChecked(True)
        elif self.selectedRow1[6] == 'Private Limited':
            self.typeRadioButton_2.setChecked(True)
        else:
            pass

        # Radio Button Group: Type of Company
        self.radioButtonGroup_Company_Type = QButtonGroup(self)
        self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_1)
        self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_2)
                                                             # <---- -------------------------------- Set typeradioButton Input from DB



        self.radioButtonTypeVerticalLayout_1.addWidget(self.typeLabel)
        self.radioButtonTypeVerticalLayout_1.addWidget(self.typeLabelBlank)  # Blank Spacing for better alignment of Vertical Radio Buttons
        self.radioButtonTypeVerticalLayout_1.addWidget(self.typeRadioButton_1)
        self.radioButtonTypeVerticalLayout_1.addWidget(self.typeRadioButton_2)

        # Vertical Layout: Status of Company
        self.radioButtonStatusVerticalLayout_2 = QVBoxLayout()
        self.statusLabel = QLabel('Status')

        # Radio Buttons: Status of Company
        # self.lineEdit_3_FileNo.setText(self.selectedRow1[0])

        self.statusRadioButton_1 = QRadioButton('Existing')
        self.statusRadioButton_2 = QRadioButton('Dissolved')
        self.statusRadioButton_3 = QRadioButton('Winding Up')

        if self.selectedRow1[7] == 'Existing':
            self.statusRadioButton_1.setChecked(True)
        elif self.selectedRow1[7] == 'Dissolved':
            self.statusRadioButton_2.setChecked(True)
        elif self.selectedRow1[7] == 'Winding Up':
            self.statusRadioButton_3.setChecked(True)
        else:
            pass
                                                                                        # <------------- Set typeradioButton Input from DB


        # Radio Button Group: Status of Company
        self.radioButtonGroup_Company_Status = QButtonGroup(self)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_1)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_2)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_3)

        self.radioButtonStatusVerticalLayout_2.addWidget(self.statusLabel)
        self.radioButtonStatusVerticalLayout_2.addWidget(self.statusRadioButton_1)
        self.radioButtonStatusVerticalLayout_2.addWidget(self.statusRadioButton_2)
        self.radioButtonStatusVerticalLayout_2.addWidget(self.statusRadioButton_3)
        #----------------------------------------------------------------------------------------------- Radio Buttons End---------------


        self.horizontalLayout_2 = QHBoxLayout()  # Horizontal Line 2

        self.horizontalLayout_2.addLayout(self.dateOfChangeVerticalLayout_1)
        self.horizontalLayout_2.addLayout(self.dateOfIncorporationVerticalLayout_1)
        self.horizontalLayout_2.addLayout(self.radioButtonTypeVerticalLayout_1)
        self.horizontalLayout_2.addLayout(self.radioButtonStatusVerticalLayout_2)



        self.mainLayoutTab1 = QVBoxLayout()  # The final main layout

        self.mainLayoutTab1.addLayout(self.comboHBoxLayout)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_1)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_2)


        # Buttons cased in an Horizontal Layout
        self.buttonHorizontal = QHBoxLayout()
        self.buttonPreviousRecord = QPushButton('Previous Record')
        self.buttonHorizontal.addWidget(self.buttonPreviousRecord)
        self.buttonNextRecord = QPushButton('Next Record')
        self.buttonHorizontal.addWidget(self.buttonNextRecord)
        self.buttonUpdateRecord = QPushButton('Update Record')
        self.buttonHorizontal.addWidget(self.buttonUpdateRecord)

        self.mainLayoutTab1.addLayout(self.buttonHorizontal)

        # Scroll Area ________________________________________________________________________________________________
        self.scrollingWidget = QWidget()
        self.scrollingWidget.setLayout(self.mainLayoutTab1)


        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollingWidget)

        self.parentMainLayout = QVBoxLayout(self)
        self.parentMainLayout.addWidget(self.scrollArea)
        # ____________________________________________________________________________________________________________________

        # self.setLayout(self.mainLayoutTab1)

        # Submit Record Button Functionality
        self.buttonPreviousRecord.clicked.connect(self.previousRecord)
        self.buttonNextRecord.clicked.connect(self.nextRecord)
        self.buttonUpdateRecord.clicked.connect(self.updateRecord)


    def setTextStatusRadioButton(self):
        print(self.selectedRow[7])

        if self.statusRadioButton_1.text() == self.selectedRow[7]:
            self.statusRadioButton_1.setChecked(True)

        elif self.statusRadioButton_2.text() == self.selectedRow[7]:
            self.statusRadioButton_2.setChecked(True)

        elif self.statusRadioButton_3.text() == self.selectedRow[7]:
            self.statusRadioButton_3.setChecked(True)
        else:
            print('These buttons do not fit the selection')


    def previousRecord(self):
        custom_message('Previous Record')

    def nextRecord(self):
        custom_message('Next Record')

    def updateRecord(self):
        custom_message('Record Updated')

    def comboBoxCompanyList(self):

        """ this connects to the db and pulls the records from the CoName field
        which is used to populate the ComboBox list. You will see a for loop below
        that is used to populate the db query into a list which is then used by the ComboBox."""

        # Database connect and query table for combobox company list
        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()
        self.query = f"SELECT CoName FROM {self.tableName}"
        self.c.execute(self.query)
        self.searchComboBox = self.c.execute(self.query)  # This is purely Python, not PyQt, the ComboBox is only set up at below using the same name

        self.comboBoxList = []  # Python List that used to add items to the searchComboBox (This is Python not PyQt)
        for company in self.searchComboBox:
            self.comboBoxList.append(company[0])



    def ifComboBoxItemSelected(self):
        self.comboBoxDeepView.currentIndexChanged.connect(self.whenComboBoxIsChanged)

    def whenComboBoxIsChanged(self):


        self.comboBoxSelection = self.comboBoxDeepView.currentText()
        # print(self.comboBoxSelection)

        try:
            self.conn = sqlite3.connect(self.databaseName)
            self.c = self.conn.cursor()

            # self.query = f"SELECT * FROM {self.tableName} WHERE CoName = {self.CoName}"
            self.query = (f""" SELECT * FROM {self.tableName} WHERE CoName = '{self.comboBoxSelection}' """)
            self.c.execute(self.query)
            self.comboBoxSelectionData = self.c.execute(self.query)
            self.comboBoxSelectionData = self.comboBoxSelectionData.fetchone()
            self.comboBoxSelectionDataFieldInput()


        except:

            print('Unable to pull data from DB')

    def comboBoxSelectionDataFieldInput(self):


        self.lineEdit_3_FileNo.setText(self.comboBoxSelectionData[0])

        self.lineEdit_coName.setText(self.comboBoxSelectionData[1])  # <-------------------------------------------

        self.lineEdit_coOldName.setText(self.comboBoxSelectionData[2])  # <-------------------------------------------

        self.lineEdit_regNo.setText(self.comboBoxSelectionData[3])  # <-------------------------------------------




        # Horizontal Line 2 : Date Change

        self.newDateEditDateOfChange = self.comboBoxSelectionData[4] #<-------------------------------------------
        self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")
        #
        # self.dateEditDateOfChange = QDateEdit()
        # self.dateEditDateOfChange.setDisplayFormat("d-MMM-yyyy")
        self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)



        # self.newDateEditDateOfChange = self.comboBoxSelectionData[4] #<-------------------------------------------
        # self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")
        # self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)



        # Horizontal Line 2 : Date Incorporated
        self.newDateEditIncorporatedDate = self.comboBoxSelectionData[5] #<-------------------------------------------
        self.setDateNewDateEditIncorporatedDateString = QDate.fromString(self.newDateEditIncorporatedDate, "d-MMM-yyyy")
        # self.dateEditIncorporatedDate = QDateEdit()
        # self.dateEditIncorporatedDate.setDisplayFormat("d-MMM-yyyy")
        self.dateEditIncorporatedDate.setDate(self.setDateNewDateEditIncorporatedDateString)



        # Vertical Layout: Type of Company
        self.radioButtonTypeVerticalLayout_1 = QVBoxLayout()
        self.typeLabel = QLabel('Type')
        self.typeLabelBlank = QLabel('')  # This is used to insert blank spacing

        # Radio Buttons: Type of Company


        if self.comboBoxSelectionData[6] == 'Limited By Shares':
            self.typeRadioButton_1.setChecked(True)
        elif self.comboBoxSelectionData[6] == 'Private Limited':
            self.typeRadioButton_2.setChecked(True)
        else:
            pass


        # Radio Button Group: Type of Company
        self.radioButtonGroup_Company_Type = QButtonGroup(self)
        self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_1)
        self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_2)
        # self.radioButtonGroup_Company_Type.checkedButton() #<------------------------------------- Radio Button Type


        # Radio Buttons: Status of Company

        if self.comboBoxSelectionData[7] == 'Existing':
            self.statusRadioButton_1.setChecked(True)
        elif self.comboBoxSelectionData[7] == 'Dissolved':
            self.statusRadioButton_2.setChecked(True)
        elif self.comboBoxSelectionData[7] == 'Winding Up':
            self.statusRadioButton_3.setChecked(True)
        else:
            pass

        # Radio Button Group: Status of Company
        self.radioButtonGroup_Company_Status = QButtonGroup(self)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_1)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_2)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_3)








