from PyQt5.QtWidgets import (QWidget)
import sqlite3

class DatabaseEngine(QWidget):
    def __init__(self):
        super().__init__()

        # Connect with Database
        self.db_name = "asa_1"
        self.db_name = f"{self.db_name}.db"
        self.tb_name = f"{self.db_name}_table"

        self.connect_to_db()
        self.create_db_table()


    def connect_to_db(self):
        """ This creates a databse if one has not been created, or
        connects to an already existing one if one exists."""

        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.conn.commit()
        print('Database has been created')

    def create_db_table(self):
        """ This function creates a new table
        is one has not been created"""

        self.field1 = 'File_No'
        self.field1Type = 'TEXT'
        self.field2 = 'Company_Name'
        self.field2Type = 'TEXT'
        self.field3 = 'Old_Company_Name'
        self.field3Type = 'TEXT'
        self.field4 = 'Registration_No'
        self.field4Type = 'TEXT'
        self.field5 = 'Date_of_Name_Change'
        self.field5Type = 'TEXT'
        self.field6 = 'Date_of_Incorporation'
        self.field6Type = 'TEXT'
        self.field7 = 'Type_of_Company'
        self.field7Type = 'TEXT'
        self.field8 = 'Status_of_Company'
        self.field8Type = 'TEXT'
        self.field9 = 'Dir_or_BOD'
        self.field9Type = 'TEXT'
        self.field10 = 'AGM_or_EGM'
        self.field10Type = 'TEXT'


        self.c.execute(f'CREATE TABLE IF NOT EXISTS {self.tb_name} ({self.field1} {self.field1Type} primary key,'
                       f'{self.field2} {self.field2Type},'
                       f'{self.field3} {self.field3Type},'
                       f'{self.field4} {self.field4Type},'
                       f'{self.field5} {self.field5Type},'                     
                       f'{self.field6} {self.field6Type},'
                       f'{self.field7} {self.field7Type},'
                       f'{self.field8} {self.field8Type},'
                       f'{self.field9} {self.field9Type},'
                       f'{self.field10} {self.field10Type})')

        self.conn.commit()
        print('Table Created')