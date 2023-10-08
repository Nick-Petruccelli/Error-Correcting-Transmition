from stats_util import StatsUtil
from PyQt5.QtWidgets import QFileDialog, QApplication
from bitstring import BitArray
from PIL import Image
import sys
import os
import io


def get_file_binary(file_name: str)->BitArray:
    """
    returns binary data from selected file
    :param file_name: path to desired file
    """
    with open(file_name, 'rb') as file:
        file_bytes = file.read()

    bit_array = BitArray(file_bytes)
    return bit_array

def get_png_from_binary(binary_data: BitArray, file_name: str)->None:
    """
    Creates png from binary data
    :param binary_data: binary data for image
    :param file_name: desired name for new image
    """
    byte_data = binary_data.tobytes()
    image = Image.open(io.BytesIO(byte_data))
    image.save(file_name+".png")


def make_binary_redundent(binary_data: BitArray, times: int)->BitArray:
    """
    takes binary data and repeats it n times
    :param binary_data: data to be made redundent
    :param times: number of times you want data to be repeated. ex) if times = 2, data will be twice as long as before
    """
    redundent_data = binary_data
    for i in range(times-1):
        redundent_data.append(binary_data)
    return redundent_data



if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name, _ = QFileDialog.getOpenFileName(None)
    file_bin= get_file_binary(file_name= file_name)
    get_png_from_binary(file_bin, "myImage")
    