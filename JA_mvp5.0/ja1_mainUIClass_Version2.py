from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QPushButton, QTextEdit,
                             QRadioButton, QVBoxLayout, QHBoxLayout,QButtonGroup,
                             QDateEdit, QApplication, QScrollArea, QGroupBox)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt


class MainUI(QWidget):
    def __init__(self):
        super().__init__()


        self.uiSetup2()
        # self.typeRadioButtonGetSelection()


    def uiSetup2(self):
        # File No
        # Horizontal Layout 1
        self.widget = QWidget()
        self.horizontal_layout_1 = QHBoxLayout()
        self.label_file_no = QLabel('File No')
        self.horizontal_layout_1.addWidget(self.label_file_no)
        self.line_edit_3_file_no = QLineEdit()
        self.horizontal_layout_1.addWidget(self.line_edit_3_file_no)

        self.label_name = QLabel('Company Name')
        self.horizontal_layout_1.addWidget(self.label_name)
        self.line_edit_co_name = QLineEdit()
        self.horizontal_layout_1.addWidget(self.line_edit_co_name)

        self.label_old_name = QLabel('Company Old Name')
        self.horizontal_layout_1.addWidget(self.label_old_name)
        self.line_edit_co_old_name = QLineEdit()
        self.horizontal_layout_1.addWidget(self.line_edit_co_old_name)

        self.label_reg_no = QLabel('Registration No')
        self.horizontal_layout_1.addWidget(self.label_reg_no)

        self.line_edit_reg_no = QLineEdit()
        self.horizontal_layout_1.addWidget(self.line_edit_reg_no)

        # Horizontal Line 2 Date of Change ############################################################################################################

        self.label_date_of_change = QLabel('Date Of Name Change')
        self.date_edit_date_of_change = QDateEdit()
        self.date_edit_date_of_change.setDisplayFormat("d-MMM-yyyy")



        # Horizontal Line 2 : Date Incorporated
        self.label_date_of_incorporation = QLabel('Date of Incorporation')
        self.date_edit_date_of_incorporation = QDateEdit()
        self.date_edit_date_of_incorporation.dateChanged.connect(self.inc_date_change_checker)
        self.date_edit_date_of_incorporation.setDisplayFormat("d-MMM-yyyy")

        # Vertical Layout for Date of Change and Incorporation
        self.date_of_change_vertical_layout_1 = QVBoxLayout()
        self.date_of_change_vertical_layout_1.addWidget(self.label_date_of_change)
        self.date_of_change_vertical_layout_1.addWidget(self.date_edit_date_of_change)

        self.date_of_incorporation_vertical_layout_1 = QVBoxLayout()
        self.date_of_incorporation_vertical_layout_1.addWidget(self.label_date_of_incorporation)
        self.date_of_incorporation_vertical_layout_1.addWidget(self.date_edit_date_of_incorporation)

        # Vertical Layout: Type of Company
        self.radio_button_co_type_vertical_layout_1 = QVBoxLayout()
        self.type_label = QLabel('Company Type')
        self.type_label_blank = QLabel('')  # This is used to insert blank spacing

        # Radio Buttons: Type of Company
        self.typeRadioButton_1 = QRadioButton('Limited By Shares')
        self.typeRadioButton_1.clicked.connect(self.typeRadioButtonClicked) # Function is in the tab1CompanyBrief File
        self.typeRadioButton_2 = QRadioButton('Private Limited')
        self.typeRadioButton_2.clicked.connect(self.typeRadioButtonClicked)# Function is in the tab1CompanyBrief File

        # Radio Button Group: Type of Company
        self.radioButtonGroup_Company_Type = QButtonGroup(self)
        self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_1)
        self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_2)

        self.radio_button_co_type_vertical_layout_1.addWidget(self.type_label)
        # self.radio_button_co_type_vertical_layout_1.addWidget(self.type_label_blank)  # Blank Spacing for better alignment of Vertical Radio Buttons
        self.radio_button_co_type_vertical_layout_1.addWidget(self.typeRadioButton_1)
        self.radio_button_co_type_vertical_layout_1.addWidget(self.typeRadioButton_2)

        # Vertical Layout: Status of Company
        self.radio_button_status_vertical_layout_2 = QVBoxLayout()
        self.status_label = QLabel('Company Status')

        # Radio Buttons: Status of Company
        self.statusRadioButton_1 = QRadioButton('Existing')
        self.statusRadioButton_1.clicked.connect(self.statusRadioButtonClicked)
        self.statusRadioButton_2 = QRadioButton('Dissolved')
        self.statusRadioButton_2.clicked.connect(self.statusRadioButtonClicked)
        self.statusRadioButton_3 = QRadioButton('Winding Up')
        self.statusRadioButton_3.clicked.connect(self.statusRadioButtonClicked)


        # Radio Button Group: Status of Company
        self.radioButtonGroup_Company_Status = QButtonGroup(self)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_1)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_2)
        self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_3)

        self.radio_button_status_vertical_layout_2.addWidget(self.status_label)
        self.radio_button_status_vertical_layout_2.addWidget(self.statusRadioButton_1)
        self.radio_button_status_vertical_layout_2.addWidget(self.statusRadioButton_2)
        self.radio_button_status_vertical_layout_2.addWidget(self.statusRadioButton_3)

        self.horizontalLayout_2 = QHBoxLayout()  # Horizontal Line 2

        self.horizontalLayout_2.addLayout(self.date_of_change_vertical_layout_1)
        self.horizontalLayout_2.addLayout(self.date_of_incorporation_vertical_layout_1)
        self.horizontalLayout_2.addLayout(self.radio_button_co_type_vertical_layout_1)
        self.horizontalLayout_2.addLayout(self.radio_button_status_vertical_layout_2)

        # Horizontal Layout 3: Registered & Business Address ######################################################################################



        self.mainLayoutTab1 = QVBoxLayout()  # The final main layout



        self.mainLayoutTab1.addLayout(self.horizontal_layout_1)
        self.mainLayoutTab1.addSpacing(20)

        self.mainLayoutTab1.addLayout(self.horizontalLayout_2)


        # Buttons cased in an Horizontal Layout
        self.buttonHorizontal = QHBoxLayout()
        self.buttonSubmitRecord = QPushButton('Submit Record')
        self.buttonHorizontal.addWidget(self.buttonSubmitRecord)
        self.buttonDeleteAllRecords = QPushButton('Delete All Records')
        self.buttonHorizontal.addWidget(self.buttonDeleteAllRecords)
        self.buttonOpenFilingSystem = QPushButton('Open Filing System')
        self.buttonHorizontal.addWidget(self.buttonOpenFilingSystem)
        self.mainLayoutTab1.addSpacing(350)
        self.mainLayoutTab1.addLayout(self.buttonHorizontal)

        # Scroll Area ________________________________________________________________________________________________
        # self.scroll = QScrollArea()
        # self.groupBox = QGroupBox()
        # self.groupBox.setLayout(self.mainLayoutTab1)
        # self.scroll.setWidget(self.groupBox)
        #
        # # self.mainLayoutTab1.addWidget(self.scroll)
        # self.mainLayoutTab2 = QVBoxLayout()
        # self.mainLayoutTab2.addWidget(self.scroll)
        # ____________________________________________________________________________________________________________________


        self.setLayout(self.mainLayoutTab1)

        # Submit Record Button Functionality
        self.buttonSubmitRecord.clicked.connect(self.submitRecordsButton)
        self.buttonOpenFilingSystem.clicked.connect(self.openFilingSystemButton)
        self.buttonDeleteAllRecords.clicked.connect(self.deleteAllRecords)








