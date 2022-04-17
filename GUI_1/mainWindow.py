import sys

from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QHBoxLayout, QVBoxLayout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(). __init__()
        self.setWindowTitle('Shopee GUI')
        self.setGeometry(800, 100, 400, 200)

        # self.openCommandPromptButton()
        # self.layout()

    # def layout(self):
        self.mainLayout = QVBoxLayout()
        self.cmdButtonLayout = QHBoxLayout()
        self.cmdButton = QPushButton('Open Scraper')
        # self.cmdButtonLayout.addWidget(self.cmdButton)

        self.mainLayout.addWidget(self.cmdButton)
        self.setLayout(self.mainLayout)

    # def openCommandPromptButton(self):




app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())