from PyQt5.QtWidgets import (QWidget, QButtonGroup)
import sqlite3
import os
from custom_message_box import custom_message
from stackedFilingSystemMVP_ja1 import StackedFilingSystem
from ja1_dbTableAndInputClass import DatabaseEngine
from ja1_mainUIClass_Version2 import MainUI


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        # Connect with the database
        # db_name = database_name, tb_name = table_name

        self.db_name = "asa_1"
        self.db_name = f"{self.db_name}.db"
        self.tb_name = f"{self.db_name}_table"

        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

        # Uses the database module to create or connect to a db and create a table

        DatabaseEngine.connect_to_db(self) # --------------------------------------------------- check if still need this, since its in
        # the db_module
        DatabaseEngine.create_db_table(self)


        MainUI.uiSetup2(self)

    def submit_records_button(self):

        self.dataClean()

        try:
            if self.FileNo != "" and self.CoName != "":
                if self.file_no_validated == 'Validated':
                    print('File No validated')
                    self.checkDuplicateCoName()
                    if self.not_duplicate == 'Validated':
                        print('Co Name is unique')
                        if self.incorporatedDateChanged == 'Validated':
                            print('Date inputed')
                            self.generateFolders()
                            self.dataUploadtoDataBase()
                        else:
                            print('Dates Not Inputed')
                    else:
                        print('Check for duplicates did not pass')
                else:
                    print('File No validation did not pass, hence we cannot proceed further')
            else:
                print('File No and Co Name missing Inputs')
        except:
            print('Validation did not pass, hence data cannot be uploaded')

    def delete_all_records_button(self):
        """ This clears all records in the current table"""

        self.c.execute(f'DELETE FROM {self.tb_name}')
        self.conn.commit()

    def folder_generator(self):
        """ This function is currently called under the Submit Records folder. This was originally designed as a button that calls the function to create all of the following
        folders; Scanned Folder, Company Folders and Company Subfolders/ Respective
        47 file folders """

        cwd = os.getcwd()  # Get current working directory to be used below

        scanned_documents = 'Scanned_Documents'
        company_name = self.co_name
        document_folder_list = ['Directors_Circular', 'Members_Meeting']



        if not os.path.isdir(f'{cwd}\\{scanned_documents}'):  # check if Scan Folder exists
            print('Scanned Docs Folder does not exists')
            os.mkdir(scanned_documents)  # if does not exist create Scan Folder
            if not os.path.isdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder'):  # Check if Company Folder exist
                print(f'{company_name} Company Main Folder does not exists')
                os.mkdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder')  # if doesn't exist, create company folder
                print(f'Created {company_name} Company Main Folder')

                if not os.path.isdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder\\_Folder_1'):  # check if scannedCompanyDocFolders exist
                    print(f'{company_name} Company Sub Folders Don\'t Exist')
                    # For Loop
                    for folder in document_folder_list:
                        os.mkdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder\\{company_name}_{folder}')

                    print(f'{company_name} Company Sub Folders Created')
                else:
                    print(f'{company_name} Company Sub Folders Already Exist')

            else:
                print(f'{company_name} Company Main Folder exists')  # if main folder and company folder exist than exit


        else:  # if main folder already exist than move on
            print('Scanned Docs Folder Already Exists')
            if not os.path.isdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder'):  # if company folder doesn't exist
                os.mkdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder')  # create company folder
                print(f'Created {company_name} Company Main Folder')

                if not os.path.isdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder\\_Folder_1'):  # check if scannedCompanyDocFolders exist
                    print(f'{company_name} Company Sub Folders Don\'t Exist')
                    # For Loop
                    for folder in document_folder_list:
                        os.mkdir(f'{cwd}\\{scanned_documents}\\{company_name}_Document_Folder\\{company_name}_{folder}')
                    print(f'{company_name} Company Sub Folders Created')
                else:
                    print(f'{company_name} Company Sub Folders Already Exist')

            else:
                print(f'{company_name} Company Main Folder exists')  # if company folder exist, do nothing and exit

            print(f'List of current Directory: {os.listdir(scanned_documents)}')

    def open_filing_tray_button(self):
        """ When this button is clicked, a new instance of the Filing System
        is opened in a new window """


        """ Now when this button is clicked, a new instance of the Filing System
        is opened in a new window, this is different form the above in that this now
        opens a new instance of the stackedwidget filing system (stackedFilingSystem_v2_forloop)"""

        self.filing_system = StackedFilingSystem()
        self.filing_system.show()

    def inc_date_change_checker(self):
        """ takes signal from dateFiled() and QDateEdit within dateFiled() and converts to text
        which is then used by the fileCopy() to validate if date has been changed
        before proceeding."""

        self.check_if_incorporated_date_changed = "Validated"

    def clean_inputs_for_upload(self):

        try:
            self.file_no = self.lineEdit_3_FileNo.text()

            try:

                if self.file_no.isalpha():
                    print('File No cannot be alphabets')
                    self.file_no_validated = 'Not Validated'

                elif self.file_no.isalpha():
                    print('File No cannot be alphabets')
                    self.file_no_validated = 'Not Validated'

                elif self.FileNo == '000':
                    print('File No cannot be 000')
                    self.file_no_validated = 'Not Validated'

                elif self.file_no == 000:
                    print('File No cannot be 000')
                    self.file_no_validated = 'Not Validated'

                elif self.file_no == '':
                    print('self.FileNo is missing an input')
                    self.file_no_validated = 'Not Validated'

                elif len(str(self.file_no)) < 3:
                    print(len(str(self.FileNo)))
                    print('File No needs to have 3 whole numbers')
                    self.file_no_validated = 'Not Validated'

                elif len(str(self.file_no)) > 3:
                    print('File No needs to have 3 whole numbers')
                    self.file_no_validated = 'Not Validated'
                else:
                    self.file_no_validated = 'Validated'
            except:
                print('File No needs to have 3 whole numbers')
        except:
            print('Error with File No input')

        self.co_name = self.lineEdit_coName.text()
        self.co_name = self.co_name.strip()
        self.co_name = self.co_name.title()
        self.co_old_name = self.lineEdit_coOldName.text()
        self.reg_no = self.lineEdit_regNo.text()
        self.date_of_change = self.dateEditDateOfChange.text()
        self.inc_date = self.dateEditIncorporatedDate.text()

        self.typeRadioButtonClicked()
        self.statusRadioButtonClicked()

    def check_for_duplicate_co_name(self):
        """ checks the company name line edit with the db for duplicate names
        before updating the db with input values"""

        try:
            self.query = (f""" SELECT co_name FROM {self.tb_name} WHERE co_name = '{self.co_name}'""")
            self.c.execute(self.query)
            self.db_co_name = self.c.execute(self.query)
            self.db_co_name = self.db_co_name.fetchone()

            if self.db_co_name:
                custom_message(f"The company {self.co_name} already exist, please check.")
            else:
                self.check_if_co_name_not_duplicate = "Validated"
        except:
            print("Unable to proceed, there is an error with the check for_check"
                  "_for_duplicate_co_name()")

    def type_radio_button_clicked(self):
        if self.type_radio_button_1.isChecked():
            self.co_type = self.type_radio_button_1.text()

        elif self.type_radio_button_2.isChecked():
            self.co_type = self.type_radio_button_2.text()

        else:
            print("Company type radio button not checked, we are unable to proceed")

    def status_radio_button_clicked(self):
        if self.status_radio_button_1.isChecked():
            self.co_status = self.status_radio_button_1.text()

        elif self.status_radio_button_2.isChecked():
            self.co_status = self.status_radio_button_2.text()

        elif self.status_radio_button_3.isChecked():
            self.co_status = self.status_radio_button_3.text()

        else:
            print("Status_radio button not checked, we are unable to proceed")

    def upload_inputs_to_database(self):

        self.c.execute(f"""INSERT INTO {self.db_name} ({self.field1},{self.field2},{self.field3},{self.field4},
                                                        {self.field5},{self.field6},{self.field7},{self.field8}) 
                                                        VALUES(?,?,?,?,?,?,?,?)""",
                                                        (self.file_no, self.co_name, self.co_old_name, self.reg_no,
                                                         self.date_name_change, self.inc_date, self.co_type, self.co_status))
        self.conn.commit()
        print(f"Database updated with values for {self.co_name}")
        self.open_filing_system_button()
