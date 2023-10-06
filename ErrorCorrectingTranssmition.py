from stats_util import StatsUtil
from PyQt5.QtWidgets import QFileDialog, QApplication
import sys
import os


def get_file_binary(file_name: str)->str:
    with open(file_name, 'rb') as file:
        file_binary = file.read()

    file_bin = ''.join(format(byte, '08b')for byte in file_binary)
    return file_bin

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name, _ = QFileDialog.getOpenFileName(None)
    file_bin= get_file_binary(file_name= file_name)
    print(len(file_bin))
    