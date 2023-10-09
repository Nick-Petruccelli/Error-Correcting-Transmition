from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from window import Ui_MainWindow
from error_correcting_transmition import ErrorCorrectingTransmition as ECT
from stats_util import StatsUtil
import sys

class MainApp(QMainWindow, Ui_MainWindow):
    sent_image_filename: str
    recived_image_filename: str
    length_of_orig: int
    
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.btn_select_image.clicked.connect(self.select_sent_image)
        self.btn_send.clicked.connect(self.set_sent_img)
        self.sel_copys.valueChanged.connect(self.copys_changed)


    def set_sent_img(self)->None:
        pixmap = QPixmap(self.sent_image_filename)
        self.dis_sent_img.setPixmap(pixmap)
        self.show()

    def set_recived_img(self)->None:
        pixmap = QPixmap(self.recived_image_filename)
        self.dis_sent_img.setPixmap(pixmap)
        self.show()

    def select_sent_image(self)->None:
        self.sent_image_filename, _ = QFileDialog.getOpenFileName(None)
        self.dis_sent_filename.setText(self.sent_image_filename.split("/")[-1])
        self.set_sent_img()

        bitarray = ECT.get_file_binary(self.sent_image_filename)
        self.dis_binary_sent.setText(bitarray.bin[0:1000]+"...")
        self.length_of_orig = len(bitarray)
        self.dis_size_of_orig.setText(f"{self.length_of_orig} (bytes)")

        length = self.length_of_orig*self.sel_copys.value()
        self.dis_size_of_redundant.setText(f"{length} (bytes)")

        self.display_prob_of_err()




    def copys_changed(self)->None:
        length = self.length_of_orig*self.sel_copys.value()
        self.dis_size_of_redundant.setText(f"{length} (bytes)")

        self.display_prob_of_err()

    def display_prob_of_err(self)->None:
        if(self.sel_copys.value()%2 == 0):
            return
        prob_of_err = self.calc_prob_of_err()
        self.dis_prob_of_err.setText(f"{prob_of_err}")

    def calc_prob_of_err(self)->float:
        copys = self.sel_copys.value()
        prob_of_bitflip = (float)(self.sel_prob_bitfilp.text())

        prob = StatsUtil.binom_dist((copys//2), copys, 1-prob_of_bitflip)
        
        prob = prob*(self.length_of_orig*8)
        return prob






        
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()