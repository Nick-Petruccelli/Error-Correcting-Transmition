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


def make_binary_redundent(binary_data: BitArray, copys: int)->BitArray:
    """
    takes binary data and repeats it n times
    :param binary_data: data to be made redundent
    :param copys: how manny copys of the data you want
    """
    redundent_data = BitArray(length=0)
    for i in range(copys):
        redundent_data.append(binary_data)
    return redundent_data

def vote_corect_data(redundent_data: BitArray, copys: int)->BitArray:
    original_data_len = (int)(len(redundent_data)/(copys))
    collapsed_data = BitArray(length=original_data_len)
    for i in range(original_data_len-1):
        num_ones = 0
        num_zeros = 0
        for j in range(copys-1):
            if(redundent_data[i+j*original_data_len] == True):
                num_ones += 1
            else:
                num_zeros += 1
        if(num_ones>num_zeros):
            collapsed_data.set(pos=i, value=True)
        else:
            collapsed_data.set(pos=i, value=False)
    return collapsed_data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name, _ = QFileDialog.getOpenFileName(None)
    file_bin = get_file_binary(file_name= file_name)
    print(len(file_bin))
    redundent_data = make_binary_redundent(file_bin, 3)
    print(len(file_bin))
    print((len(redundent_data)))
    print(file_bin[0:10].bin)
    print(redundent_data[0:10].bin)
    collapsed_data = vote_corect_data(redundent_data, 3)
    print(collapsed_data[0:10].bin)
    get_png_from_binary(collapsed_data, "myImage")
    