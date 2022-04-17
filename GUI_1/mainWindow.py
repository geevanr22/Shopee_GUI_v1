# Shopee Scraper with a GUI using PySide6

from PySide6.QtWidgets import (QMainWindow, QDialog, QApplication, QPushButton, QHBoxLayout, QVBoxLayout)
import sys
from Product_Scraper import ProductScraperClass



class MainWindow(QDialog):
    def __init__(self):
        super(). __init__()
        self.setWindowTitle('Shopee GUI')
        self.setGeometry(800, 100, 400, 200)

        # Initiate searchPushButton widget
        self.searchButton = QPushButton('Search')

        # connect searchButton to function that calls the openBrowser module and starts the browser and search functions
        self.searchButton.clicked.connect(self.searchButtonFunctionCall)

        self.layout()


    def layout(self):
        # initiate main layout
        self.mainLayout = QVBoxLayout()

        # Search Button Layout
        self.searchButtonLayout = QHBoxLayout()
        self.searchButtonLayout.addWidget(self.searchButton)

        # add search button to main layout
        self.mainLayout.addLayout(self.searchButtonLayout)

        # set main layout to set layout
        self.setLayout(self.mainLayout)


    def searchButtonFunctionCall(self):
        # calls the openBrowser module where the selenium scraper can take over
        print('checking if search button works')
        init_1 = ProductScraperClass('sex toys', 1)
        init_1.open_search_page()












app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())