from PyQt5.QtWidgets import QFileDialog, QApplication
from bitstring import BitArray
from PIL import Image
from random import random
import sys
import io

class ErrorCorrectingTransmition:
    @staticmethod
    def get_file_binary(file_name: str)->BitArray:
        """
        returns binary data from selected file
        :param file_name: path to desired file
        """
        with open(file_name, 'rb') as file:
            file_bytes = file.read()

        bit_array = BitArray(file_bytes)
        return bit_array
    
    @staticmethod
    def sim_file_transmition(file_path: str, copys: int, prob_of_bitflip: float)->bool:
        file_bin = ErrorCorrectingTransmition.get_file_binary(file_name= file_path)
        redundent_data = ErrorCorrectingTransmition.make_binary_redundant(file_bin, copys)
        collapsed_data = ErrorCorrectingTransmition.vote_corect_data(redundent_data, copys)

        for i in range(len(redundent_data)):
            if(random() <= prob_of_bitflip):
                redundent_data[i] = not redundent_data[i]

        for i in range(len(file_bin)):
            if(file_bin[i] != collapsed_data[i]):
                return False

        ErrorCorrectingTransmition.get_png_from_binary(collapsed_data, "myImage")
        return True


    @staticmethod
    def get_png_from_binary(binary_data: BitArray, file_name: str)->None:
        """
        Creates png from binary data
        :param binary_data: binary data for image
        :param file_name: desired name for new image
        """
        byte_data = binary_data.tobytes()
        image = Image.open(io.BytesIO(byte_data))

        image.save(file_name+".png")
        image.close()

    @staticmethod
    def make_binary_redundant(binary_data: BitArray, copys: int)->BitArray:
        """
        takes binary data and repeats it n times
        :param binary_data: data to be made redundant
        :param copys: how manny copys of the data you want
        """
        redundant_data = BitArray(length=0)
        for i in range(copys):
            redundant_data.append(binary_data)
        return redundant_data

    @staticmethod
    def vote_corect_data(redundant_data: BitArray, copys: int)->BitArray:
        """
        takes redundant binary data and takes returns the reduced binary data based on
            which bit was most common in the redundant data
        :param redundant_data: binary data that is repeated
        :param copys: number of copys of the data
        """
        original_data_len = int(len(redundant_data)/(copys))
        collapsed_data = BitArray(length=original_data_len)
        for i in range(original_data_len-1):
            num_ones = 0
            num_zeros = 0
            for j in range(copys-1):
                if(redundant_data[i+j*original_data_len] == True):
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
    #file_bin = ErrorCorrectingTransmition.get_file_binary(file_name= file_name)
    #redundent_data = ErrorCorrectingTransmition.make_binary_redundant(file_bin, 3)
    #collapsed_data = ErrorCorrectingTransmition.vote_corect_data(redundent_data, 3)
    #collapsed_data.set(pos= 0, value=True)
    ErrorCorrectingTransmition.sim_file_transmition(file_name, 3)
    #ErrorCorrectingTransmition.get_png_from_binary(collapsed_data, "myImage")
    