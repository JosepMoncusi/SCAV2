# Task1 - RGB/YUV translator
print('\n TASK 1:')

def translator(ry, gu, bv, type):
    #Depending on the iput's type it does the convenient coversion as the formula explicites
    if type == 'RGB':
        y = 0.299 * ry + 0.587 * gu + 0.114 * bv
        u = 0.492 * (bv - y)
        v = 0.887 * (ry - y)

        return y, u, v

    elif type == 'YUV':

        r = ry + 1.14 * bv
        g = ry - 0.395 * gu - 0.581 * bv
        b = ry + 2.033 * gu

        return r, g, b

    else:
        print('type must be RGB/YUV')


rgb2yuv = translator(10, 145, 80, 'RGB')
yuv2rgb = translator(rgb2yuv[0], rgb2yuv[1], rgb2yuv[2], 'YUV')
print(rgb2yuv)
print(yuv2rgb)

# Task2 - ffmpeg resize
print('\n TASK 2:')

# I've tried to use the library python-ffmpeg since now i doesn't have it installed on a native ubuntu.
# A priori, the code below should work as it is commented. Nonetheless, it seems like in the python-ffmpeg module
# the attribute .input() does not exist. Same thing happens on the TASK 4.

import ffmpeg

def resize_and_reduce_quality_ffmpeg(input_image, output_image, width, height, quality):
    try:
        (
            ffmpeg
            .input(input_image) #We open the image given as a parameter of the method
            .output(output_image, vf=f'scale={width}:{height}', q=quality) #vf for fornat, q for compression
            .run(overwrite_output=True) #Execute the ffmpeg command. If an output already exists it will be rewritten
        )

        print(f"SUCCESS. Saved to {output_image}")
    except Exception as e:
        print(f"ERROR: {e}")


input_image = 'messi.jpg'
output_image = 'output.jpg'
width = 800
height = 600
quality = 20

resize_and_reduce_quality_ffmpeg(input_image, output_image, width, height, quality)

# Task3 - Serpentine
print('\n TASK 3:')

import numpy as np


def serpentina(matrix):
    size = len(matrix)
    result = []

    for i in range(size):

        if i % 2 == 0:
            for j in range(i + 1):
                result.append(matrix[i - j][j]) #Move horitzontally to the right side
        else:
            for j in range(i + 1):
                result.append(matrix[j][i - j]) #Move vertically downwards

    for i in range(1, size):
        if i % 2 == 0:
            for j in range(size - i):
                result.append(matrix[i + j][size - 1 - j]) #Move diagonally upwards-right
        else:
            for j in range(size - i):
                result.append(matrix[size - 1 - j][i + j]) #Move diagonally downwads-left

    return result


# Using this matrix the result should be: [1, 2, 3, 4,..., 63, 64]
matrix = np.array([[1, 2, 6, 7, 15, 16, 28, 29],
                   [3, 5, 8, 14, 17, 27, 30, 43],
                   [4, 9, 13, 18, 26, 31, 42, 44],
                   [10, 12, 19, 25, 32, 41, 45, 54],
                   [11, 20, 24, 33, 40, 46, 53, 55],
                   [21, 23, 34, 39, 47, 52, 56, 61],
                   [22, 35, 38, 48, 51, 57, 60, 62],
                   [36, 37, 48, 50, 58, 59, 63, 64]])

print(serpentina(matrix))

# Task4 - ffmpeg transform
print('\n TASK 4:')


def transform_to_bw_and_compress(input_image, output_image):
    try:
        # Apply the B/W filter and hardest compression settings
        (
            ffmpeg.input(input_image)
            .output(output_image, vf='format=gray', crf=51)  #vf for format,  crf=51 for maximum compression
            .run(overwrite_output=True) #Execute the ffmpeg command. If an output already exists it will be rewritten
        )

        print(f"SUCCESS. Saved to {output_image}")
    except Exception as e:
        print(f"ERROR: {e}")



input_image = 'messi.jpg'
output_image = 'output_bw_compressed.jpg'

transform_to_bw_and_compress(input_image, output_image)

# Task5 - Run-length encoding
print('\n TASK 5:')


def run_length_encode(data):
    encoded_data = bytearray()
    i = 0
    data_length = len(data)

    while i < data_length:
        count = 1
        while i + 1 < data_length and data[i] == data[i + 1]: #'while' keeps going when the byte repeats
            count += 1 #Counter for the number of repeated bytes
            i += 1

        encoded_data.append(count) #Number of repeated bytes. As in run-lenght encoding
        encoded_data.append(data[i]) #The bytes that are repeated. As in run-lenght encoding

        i += 1

    return bytes(encoded_data)


original = bytes([1, 3, 3, 2, 2, 2, 2, 4, 4, 4, 1, 1])
encoded = run_length_encode(original)
print(f"Original bytes: {original}")
print(f"Encoded bytes: {encoded}")

# Task6 - DCT class
print('\n TASK 6:')


import numpy as np


# Define a class for DCT (Discrete Cosine Transform) conversion
class DCTConverter:
    def __init__(self, block_size=8):
        self.block_size = block_size #Constructor to initialize the class

    def dct2(self, image):
        #Perform 2D DCT - block
        rows, cols = image.shape
        dct_result = np.zeros((rows, cols), dtype=float)


        for u in range(rows):
            for v in range(cols):
                sum_value = 0.0

                for x in range(rows):
                    for y in range(cols):
                        # Compute cosine terms for both dimensions
                        cos_term_x = np.cos((2 * x + 1) * u * np.pi / (2 * rows))
                        cos_term_y = np.cos((2 * y + 1) * v * np.pi / (2 * cols))

                        sum_value += image[x, y] * cos_term_x * cos_term_y #DCT formula's sum

                alpha_u = 1.0 if u == 0 else np.sqrt(2) / 2
                alpha_v = 1.0 if v == 0 else np.sqrt(2) / 2

                sum_value *= (alpha_u * alpha_v) / (rows * cols) #Multiply by alpha values and scale

                dct_result[u, v] = sum_value #Store the result

        return dct_result

    def convert(self, input_data):
        #Perform DCT conversion - entire data
        rows, cols = input_data.shape
        result = np.zeros((rows, cols), dtype=float)


        for i in range(0, rows, self.block_size):
            for j in range(0, cols, self.block_size):
                block = input_data[i:i + self.block_size, j:j + self.block_size] #Extract a block of data
                dct_block = self.dct2(block) # Apply DCT

                result[i:i + self.block_size, j:j + self.block_size] = dct_block #Store the result

        return result



input_data = np.random.random((4,4))
dct_converter = DCTConverter(block_size=8)

dct_result = dct_converter.convert(input_data)
print("DCT Result:", dct_result)

