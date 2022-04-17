from PyQt5.QtWidgets import (QListWidget, QWidget, QPushButton, QDateEdit,
                             QVBoxLayout, QHBoxLayout, QListWidgetItem,
                             QComboBox, QLabel, QRadioButton, QButtonGroup)

from PyQt5.QtCore import *
import os
import shutil
import sqlite3
import json
from custom_message_box import custom_message

""" Filing Window"""
""" This is for the separate window, once the Submit Record button is clicked on the Company Brief window.This window
    should be a stacked widget that switches between the 48 folders. Therefore each stacked widget represents a file
    tray that copies files to it's respective folder(one of the 48 folders. The combobox should be pulling information
    from the list of Company Folders (currently it pulls from the DB CoName field) that have been generated thus far, hence 
    the Company Name in DB = Company Folder Names = Company Names in the Filing System Combo Box ."""


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            self.links = []
            print(event.mimeData().urls())

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.links.append(str(url.toLocalFile()))
                else:
                    self.links.append(str(url.toString()))

            self.addItems(self.links)
        else:
            event.ignore()


class FilingSystem(QWidget):

    def __init__(self, fileFolderName):
        super().__init__()

        # self.setGeometry(1960, 600, 380, 400) # refer to stackedFilingSystem

        # Connect with Database
        self.databaseName = 'ja1'
        self.databaseName = f'{self.databaseName}.db'
        self.tableName = 'JA1'

        # Date Filed
        self.fileDateLabel = QLabel('Date Filed')
        self.fileDateEdit = QDateEdit()

        # File Folder Name
        self.fileFolderName = f'_{fileFolderName}'

        # File Name
        self.fileName = self.fileFolderName

        # self.titleRespectiveToStackedWidget()
        self.title = QLabel(f"{fileFolderName.replace('_',' ')}")  # Title for the respective Stacked Widget, which follows the File Folder Name i.e. 'Directors Circular'
        self.title.setAlignment(Qt.AlignCenter)

        self.comboMethod()
        self.fileTray()
        self.buttons()
        self.radio_button_dc_mm()
        self.layout()
        self.dateFiled()


    def titleRespectiveToStackedWidget(self):
        """This function is to covert the File Folder name generated
        as the Filing System instance constructor to the Stacked Window respective title
        i.e. 'Directors_Circular ---> Directors Circular Folder """

        title1 = self.fileFolderName.split('_')[0]
        title2 = self.fileFolderName.split('_')[1]
        self.title = f'{title1} {title2} Folder'
        return self.title

    def radio_button_dc_mm(self):# radio buttons for directors circular and members meeting

        # Radio Buttons: Directors Circular & Members Meeting
        self.hradio_button_dc1 = QRadioButton("DR")
        self.hradio_button_dc1.clicked.connect(self.hradio_button_dc_Clicked) # this retrieves the selected input
        self.hradio_button_dc2 = QRadioButton("BOD")
        self.hradio_button_dc2.clicked.connect(self.hradio_button_dc_Clicked) # this retrieves the selected input

        self.hradio_button_mm1 = QRadioButton("AGM")
        self.hradio_button_mm1.clicked.connect(self.hradio_button_mm_Clicked) # this retrieves the selected input
        self.hradio_button_mm2 = QRadioButton("EGM")
        self.hradio_button_mm2.clicked.connect(self.hradio_button_mm_Clicked) # this retrieves the selected input


        # Radio Button Grouping Director Circular (DR and BOD buttons)
        self.radio_button_group_dc = QButtonGroup(self)
        self.radio_button_group_dc.addButton(self.hradio_button_dc1)
        self.radio_button_group_dc.addButton(self.hradio_button_dc2)

        # Radio Button Grouping Members Meeting (AGM and EGM buttons)
        self.radio_button_group_mm = QButtonGroup(self)
        self.radio_button_group_mm.addButton(self.hradio_button_mm1)
        self.radio_button_group_mm.addButton(self.hradio_button_mm2)

    def hradio_button_dc_Clicked(self):

        if self.hradio_button_dc1.isChecked():
            self.company = self.comboBoxListCompany
            self.dr_or_bod = self.hradio_button_dc1.text()
        elif self.hradio_button_dc2.isChecked():
            self.company = self.comboBoxListCompany
            self.dr_or_bod = self.hradio_button_dc2.text()

        else:
            pass

        try:
            self.c.execute(f"""UPDATE {self.tableName} SET DR_or_BOD = '{self.dr_or_bod}' WHERE CoName='{self.company}' """)
            self.conn.commit()
            print('DB Updated with DR or BOD')
        except:
            print('Not able to update db with Directors Circular selection')


    def hradio_button_mm_Clicked(self):

        if self.hradio_button_mm1.isChecked():
            self.company = self.comboBoxListCompany
            self.agm_or_egm = self.hradio_button_mm1.text()
        elif self.hradio_button_mm2.isChecked():
            self.company = self.comboBoxListCompany
            self.agm_or_egm = self.hradio_button_mm2.text()
        else:
            pass

        try:
            self.c.execute(f"""UPDATE {self.tableName} SET AGM_or_EGM = '{self.agm_or_egm}' WHERE CoName = '{self.company}' """)
            self.conn.commit()
            print('DB Updated with AGM or EGM')
        except:
            print('Not able to update db with Members Meeting selection')

    def dateFiled(self):
        """ sets up date label, date widget, and also checks if date has been changed. When changed,
        a signal connects to dateChanged() function to call out the date in text format. This date
        in text format is then used by the fileCopy() function which uses an if statement to check
        if date has been changed or else would not let you move to the next step."""

        self.hdateLayout.addWidget(self.fileDateLabel)
        self.hdateLayout.addWidget(self.fileDateEdit)
        self.fileDateEdit.dateChanged.connect(self.dateChanged)

    def dateChanged(self):
        """ takes signal from dateFiled() and QDateEdit within dateFIled() and converts to text
        which is then used by the fileCopy() to validate if date has been changed
        before proceeding."""
        self.date = self.fileDateEdit.text()
        return self.date

    def comboMethod(self):
        """ this connects to the db and pulls the records from the CoName field
        which is used to populate the ComboBox list. You will see a for loop below
        that is used to populate the db query into a list which is then used by the ComboBox."""

        # Database connect and query table for combobox company list
        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()
        self.query = f"SELECT CoName FROM {self.tableName}"
        self.c.execute(self.query)
        self.searchComboBox = self.c.execute(
            self.query)  # This is purely Python, not PyQt, the ComboBox is only set up at below using the same name

        self.comboBoxList = []  # Python List that used to add items to the searchComboBox (This is Python not PyQt)
        for company in self.searchComboBox:
            self.comboBoxList.append(company[0])
            self.comboBoxListCompany = company[0]

        # ComboBox Setup
        self.labelSearchComboBox = QLabel('Search Company')
        self.searchComboBox = QComboBox()
        self.searchComboBox.addItems(self.comboBoxList)  # items from the CoName in db are added to the searchComboBox from a Python List

        # ComboBox Layout
        self.hlayoutComboBox = QHBoxLayout()
        self.hlayoutComboBox.addWidget(self.labelSearchComboBox)
        self.hlayoutComboBox.addWidget(self.searchComboBox)

        """Additional Notes: There are two parts here, one is the db, db query, and the for loop that gets the 
        db content and then stores in a list. All this is python, and done before the Qt.ComboBox is set up. So maybe we 
        can break them apart to make it more transferable."""

    def fileTray(self):
        """ sets up the ListWidget for the file tray and
        retrieves the text of the current selected item in the list widget"""

        # ListWidget 1
        self.label_FileTray1 = QLabel('Directors Circular')
        self.listWidget_FileTray1 = ListBoxWidget()
        self.item_FileTray1 = QListWidgetItem(self.listWidget_FileTray1.currentItem())
        self.item_FileTray1 = self.item_FileTray1.text()

    def buttons(self):
        # PushButton
        self.clearListButton = QPushButton('Clear List')
        self.clearListButton.clicked.connect(self.clearList)
        self.fileCopyButton = QPushButton('Copy File')
        self.fileCopyButton.clicked.connect(self.fileCopy)
        # self.fileListButton = QPushButton('File List')
        # self.fileListButton.clicked.connect(self.savedFilePathLink)

    def layout(self):
        """Setup for all the layouts in this class"""
        # Layout
        self.mainLayoutTab2 = QVBoxLayout()

        self.htitleLabelLayout = QHBoxLayout()
        self.htitleLabelLayout.addWidget(self.title)
        self.mainLayoutTab2.addLayout(self.htitleLabelLayout)

        # Radio Buttons for Directors Circular and Members Meeting selection
        self.hlayout_radio_button = QHBoxLayout()
        self.mainLayoutTab2.addSpacing(10)
        self.hlayout_radio_button.addWidget(self.hradio_button_dc1)
        self.hlayout_radio_button.addWidget(self.hradio_button_dc2)
        self.hlayout_radio_button.addWidget(self.hradio_button_mm1)
        self.hlayout_radio_button.addWidget(self.hradio_button_mm2)
        self.mainLayoutTab2.addLayout(self.hlayout_radio_button)


        self.hdateLayout = QHBoxLayout()
        self.mainLayoutTab2.addSpacing(10)

        self.mainLayoutTab2.addLayout(self.hlayoutComboBox)  # You remove this, the searchComboBox will fail, you will not be able to get the selected Company name item
        self.mainLayoutTab2.addSpacing(8)
        self.mainLayoutTab2.addLayout(self.hdateLayout)
        self.mainLayoutTab2.addWidget(self.listWidget_FileTray1)

        # self.mainLayoutTab2.addWidget(self.saveFileButton)
        self.mainLayoutTab2.addWidget(self.fileCopyButton)
        self.mainLayoutTab2.addWidget(self.clearListButton)
        # self.mainLayoutTab2.addWidget(self.fileListButton)
        self.setLayout(self.mainLayoutTab2)

    def clearList(self):
        """ Clears all from the list, ListWidget does not have clear
        selected item. Need to stop more than one file drop! But
        I am coming to find out that there might be a way to clear
        each selected item one at a time"""

        try:
            self.selectedItemToBeCleared = self.listWidget_FileTray1.currentItem()
            self.listWidget_FileTray1.clear()
        except:
            custom_message('Unable to clear list, check the clearSelectedListItem method')

    def fileCopy(self):
        """ Folder & File Hierarchy: ScannedDocs/CompanyFolder/CompanyFileNameFolder/CompanyFileName.pdf
         i.e. CompanyFolder = Tesla, CompanyFileNameFolder = Tesla_Directors_Circular, CompanyFileName = date_Tesla_directors_circular_1"""

        """The largest method in this class. Copies the selected file dropped
        into the listwidget/filetray to the respective folder, in this order:
        ScannedDocs/Company/CompanyDoc/File.
        The file will be using a formatted date at the beginning of the filename
        which the user would need to select before saving/copying the file."""

        """Checks if the date has been changed"""
        try:
            print(self.date)
        except:
            custom_message('Did you forget to set the date?')

        try:

            """Retrieves the number of files dropped into the file tray, 
            this count is then used to prevent either trying to save
            with 0 or more than 1 file dropped"""

            self.listWidget_FileTray1Count = self.listWidget_FileTray1.count()
            print(f'No of file: {self.listWidget_FileTray1Count}')

            if self.listWidget_FileTray1Count == 1:

                """" Gets the text of the selected item in the listwidget,
                 this will be used as the source file that is to be copied.
                 Not really sure if we need to do this"""

                self.item_FileTray1 = QListWidgetItem(self.listWidget_FileTray1.currentItem())
                self.item_FileTray1 = self.item_FileTray1.text()

                """Retrieves the name selected on the ComboBoxList, 
                which is used as the Company Name for Company Folder"""

                self.comboBoxCoNameSelection = self.searchComboBox.currentText()
                self.companyFolderName = f'{self.comboBoxCoNameSelection}_DocFolder'

                """Variable for the SubFolder one level below the Company Folder,
                 will have 48 of these which is 47 plus 1 Miscellaneous"""
                # self.fileFolderName = '_Directors_Circular' -----> Moved to the top as part of Class Variable

                """Variable for file name extension for all those in the Directors Circular Folder"""
                # self.fileName = 'DirectorsCircular' -----> Moved to the top as part of Class Variable

                # File Date (Each File is supposed to have a date associated to it)
                date = self.date
                date1 = date.split('/')[0]
                date2 = date.split('/')[1]
                date3 = date.split('/')[2]
                self.directorsCircularFileDate = f'{date1}_{date2}_{date3}_'

                self.directorsCircularFolderPath = f'ScannedDocs\\{self.companyFolderName}\\{self.comboBoxCoNameSelection}{self.fileFolderName}'
                self.directorsCircularFolderFileCount = len(os.listdir(self.directorsCircularFolderPath))

                # Destination directory
                self.newDirectory = f'ScannedDocs\\{self.companyFolderName}\\{self.comboBoxCoNameSelection}{self.fileFolderName}\\{self.directorsCircularFileDate}{self.fileName}_{self.directorsCircularFolderFileCount + 1}.pdf'

                # Copy from source to destination
                shutil.copyfile(self.item_FileTray1, self.newDirectory)

                custom_message(f'{self.fileName} dated {self.directorsCircularFileDate} has been successfully saved to {self.fileFolderName} in {self.comboBoxCoNameSelection} folder')

                self.savedFilePathLink()
                self.fileFolderListFunction()
                self.uploadFileFolderList()

            elif self.listWidget_FileTray1Count == 0:
                custom_message('There are no files to be copied, you need to drop a file.')

            elif self.listWidget_FileTray1Count > 1:  # Please test this code, it was == 0 previously
                custom_message('You have more than one file, you can only copy one file at a time.')

        except:
            custom_message('Unable to save file, kindly check your code under the try accept block for fileCopy()')
        # print(self.newDirectory)

    def savedFilePathLink(self):
        try:
            print(self.newDirectory)
        except:
            print('Cannot print saved file path')

    def fileFolderListFunction(self):
        try:
            self.fileFolderList = os.listdir(f'ScannedDocs\\{self.companyFolderName}\\{self.comboBoxCoNameSelection}'
                                             f'{self.fileFolderName}')
            print(f'FileFolderList: self.fileFolderList:: {self.fileFolderList}')
        except:
            print('Unable to print Directory Listing for Folder')

    def uploadFileFolderList(self):

        print(f'Upload Folder Trial Working at line 302')
        print(f'self.tableName: {self.tableName}')
        print(f'File Folder Name:{self.fileFolderName}')
        self.fileFolderListFieldName = self.fileFolderName
        # self.fileFolderListFieldName = (f'{self.fileFolderListFieldName[1]}_{self.fileFolderListFieldName[2]}')
        print(f'File Folder List Field Name: {self.fileFolderListFieldName}')
        print(f'self.comboBoxCoNameSelection: {self.comboBoxCoNameSelection}')
        print(f'self.fileFolderList:: {self.fileFolderList}')

        self.listjSon = json.dumps(self.fileFolderList)

        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()

        print("Test Line 310")

        # try:
        #     self.c.execute(f"""UPDATE {self.tableName} SET {self.fileFolderListFieldName} =
        #      '{self.listjSon}' WHERE CoName='{self.comboBoxCoNameSelection}' """)
        #
        #     print(f"DataBase successfully updated with {self.comboBoxCoNameSelection}'s"
        #           f" {self.fileFolderListFieldName} folder file lists.")
        #
        # except:
        #
        #     print(f'Unable to update DB with File Folder List for Company: '
        #           f'{self.comboBoxCoNameSelection}\'s {self.fileFolderListFieldName} folder.')
        #
        #
        #
        # self.conn.commit()

    def uploadDirector_Members_Selection(self):

        try:
            self.c.execute(f"""UPDATE {self.tableName} SET DR_or_BOD = '{self.dr_or_bod}' WHERE CoName='{self.company}' """)
            self.conn.commit()
            print('DB Updated with DR or BOD')
        except:
            print('Not able to update db with Directors Circular selection')

        try:
            self.c.execute(f"""UPDATE {self.tableName} SET AGM_or_EGM = {self.agm_or_egm} WHERE CoName = {self.company}""")
            self.conn.commit()
            print('DB Updated with AGM or EGM')
        except:
            print('Not able to update db with Members Meeting selection')


