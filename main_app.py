from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from window import Ui_MainWindow
from error_correcting_transmition import ErrorCorrectingTransmition as ECT
from stats_util import StatsUtil
import sys
import os

class MainApp(QMainWindow, Ui_MainWindow):
    sent_image_filename: str
    copys: int
    prob_of_bitflip: float
    length_of_orig: int
    num_of_acctual_errs: int
    
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.copys=self.sel_copys.value()
        self.prob_of_bitflip=float(self.sel_prob_bitfilp.text())
        self.num_of_acctual_errs=0
        self.length_of_orig=0
        
        
    @pyqtSlot()
    def on_btn_select_image_clicked(self)->None:
        self.sent_image_filename, _ = QFileDialog.getOpenFileName(None)
        self.dis_sent_filename.setText(self.sent_image_filename.split("/")[-1])
        self.set_sent_img()

        bitarray = ECT.get_file_binary(self.sent_image_filename)
        self.dis_binary_sent.setText(bitarray.bin[0:1000]+"...")
        self.length_of_orig = len(bitarray)
        self.dis_size_of_orig.setText(f"{self.length_of_orig} (bytes)")

        self.copys = self.sel_copys.value()
        length = self.length_of_orig*self.copys
        self.dis_size_of_redundant.setText(f"{length} (bytes)")

        self.display_prob_of_err()

    @pyqtSlot(int)
    def on_sel_copys_valueChanged(self)->None:
        self.copys = self.sel_copys.value()

        length = self.length_of_orig*self.copys
        self.dis_size_of_redundant.setText(f"{length} (bytes)")

        self.display_prob_of_err()

    @pyqtSlot()
    def on_sel_prob_bitfilp_editingFinished(self)->None:
        self.prob_of_bitflip = float(self.sel_prob_bitfilp.text())
        self.display_prob_of_err()


    @pyqtSlot()
    def on_btn_send_clicked(self):

        copys = self.copys
        self.prob_of_bitflip = float(self.sel_prob_bitfilp.text())
        for i in range(100):
            is_correct = ECT.sim_file_transmition(self.sent_image_filename, copys, self.prob_of_bitflip)
            if(is_correct):
                break
            self.num_of_acctual_errs = self.num_of_acctual_errs+1
        num_errs = self.num_of_acctual_errs
        self.dis_actual_errs.setText(f"{num_errs}")
        
        if(not is_correct):
            return
        self.set_recived_img()
        
        length_of_path = len(self.sent_image_filename)-len(self.sent_image_filename.split("/")[-1])
        recived_image_path = self.sent_image_filename[0:length_of_path]+"myImage.png"
        
        recived_binary = ECT.get_file_binary(recived_image_path)
        self.dis_binary_recevied.setText(recived_binary.bin[0:1000])
        


    def set_sent_img(self)->None:
        pixmap = QPixmap(self.sent_image_filename)
        self.dis_sent_img.setPixmap(pixmap)
        self.show()

    def set_recived_img(self)->None:
        pixmap = QPixmap("myImage.png")
        self.dis_recived_img.setPixmap(pixmap)
        self.show()

    def display_prob_of_err(self)->None:
        if(self.length_of_orig == 0):
            return
        if(self.copys%2 == 0):
            return
        prob_of_err = self.calc_prob_of_err()
        self.dis_prob_of_err.setText(f"{prob_of_err}%")

    def calc_prob_of_err(self)->float:
        copys = self.copys

        prob = StatsUtil.binom_dist((copys//2), copys, 1-self.prob_of_bitflip)
        
        prob = prob*(self.length_of_orig*8)*100
        return prob
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    try:
        os.remove(os.getcwd()+"/myImage.png")
    except:
        pass
