from PyQt5.QtWidgets import QMainWindow, QApplication
from window import Ui_MainWindow
import sys

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        
        self.send_button.clicked.connect(lambda x: self.helow("nick"))
        self.copys_select.valueChanged.connect(lambda x: print("change"))

    def helow(self, name: str):
        print(f"hellow {name}")
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()