from PyQt5.QtWidgets import QMessageBox

def custom_message(input):
    message = QMessageBox()
    message.setText(f'{input}')
    message.setIcon(QMessageBox.Information)
    message = message.exec_()



