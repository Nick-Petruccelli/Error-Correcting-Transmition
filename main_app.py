from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        loadUi("MainUI.ui", self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()