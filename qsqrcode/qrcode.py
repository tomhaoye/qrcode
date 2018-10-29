#!/usr/bin/python
from PIL import Image
from math import sqrt
from .constant import level_index
from .constant import format_info_str
from .constant import version_info_str
from .constant import alignment_location


class Qrcode:
    level = None
    qrcode = None
    version = None
    encode_data = None
    data_matrix = None
    mask_id = None
    length = 0
    size = ()

    def resize(self, size):
        self.qrcode.resize((size, size), Image.ANTIALIAS)
        return self.qrcode

    def generate(self, path):
        self.qrcode.save(path)
        return

    def __init__(self, message, level='L'):
        self.level = level_index[level]

        def decide_version(message):
            self.version = 7
            self.length = 21 + 4 * (self.version - 1)
            self.size = (self.length, self.length)

        def draw():
            def build_locate_sign():
                for i in range(7):
                    self.qrcode.putpixel((0, i), 0)
                    self.qrcode.putpixel((6, i), 0)
                    self.qrcode.putpixel((0, i + 14 + 4 * (self.version - 1)), 0)
                    self.qrcode.putpixel((6, i + 14 + 4 * (self.version - 1)), 0)
                    self.qrcode.putpixel((14 + 4 * (self.version - 1), i), 0)
                    self.qrcode.putpixel((20 + 4 * (self.version - 1), i), 0)
                    self.qrcode.putpixel((i, 0), 0)
                    self.qrcode.putpixel((i, 6), 0)
                    self.qrcode.putpixel((i, 14 + 4 * (self.version - 1)), 0)
                    self.qrcode.putpixel((i, 20 + 4 * (self.version - 1)), 0)
                    self.qrcode.putpixel((i + 14 + 4 * (self.version - 1), 0), 0)
                    self.qrcode.putpixel((i + 14 + 4 * (self.version - 1), 6), 0)

                for j in range(2, 5):
                    for k in range(2, 5):
                        self.qrcode.putpixel((j, k), 0)
                        self.qrcode.putpixel((j + 14 + 4 * (self.version - 1), k), 0)
                        self.qrcode.putpixel((j, k + 14 + 4 * (self.version - 1)), 0)

            def build_time_sign():
                for i in range(3 + 2 * (self.version - 1)):
                    self.qrcode.putpixel((8 + 2 * i, 6), 0)
                    self.qrcode.putpixel((6, 8 + 2 * i), 0)
                self.qrcode.putpixel((8, 13 + 4 * (self.version - 1)), 0)

            def build_alignment_sign():
                point_matrix = []
                if alignment_location[self.version]:
                    for i in alignment_location[self.version]:
                        for j in alignment_location[self.version]:
                            point_matrix.append((j, i))
                matrix_len = len(point_matrix)
                for index in range(len(point_matrix)):
                    if index == 0 or index == sqrt(matrix_len) - 1 or index == matrix_len - (sqrt(matrix_len) - 1) - 1:
                        continue
                    else:
                        self.qrcode.putpixel(point_matrix[index], 0)
                        for offset in range(-2, 3):
                            self.qrcode.putpixel((point_matrix[index][0] + offset, point_matrix[index][1] - 2), 0)
                            self.qrcode.putpixel((point_matrix[index][0] + offset, point_matrix[index][1] + 2), 0)
                            self.qrcode.putpixel((point_matrix[index][0] - 2, point_matrix[index][1] + offset), 0)
                            self.qrcode.putpixel((point_matrix[index][0] + 2, point_matrix[index][1] + offset), 0)

            def level_and_mask_draw():
                for format_i in range(len(format_info_str[self.level][self.mask_id])):
                    self.qrcode.putpixel((format_i if format_i < 6 else (
                        format_i + 1 if format_i < 8 else self.length + (5 - format_i)), 8), 1 - int(
                        format_info_str[self.level][self.mask_id][format_i]))
                    # todo
                    self.qrcode.putpixel((8, format_i), 1 - int(format_info_str[self.level][self.mask_id][format_i]))
                self.qrcode.putpixel((self.length - 8, 8), 1 - int(format_info_str[self.level][self.mask_id][7]))

            def version_info_draw():
                if self.version > 6:
                    _version_info = version_info_str[self.version][::-1]
                    for num_i in range(len(_version_info)):
                        self.qrcode.putpixel((num_i // 3, num_i % 3 + self.length - 11), 1 - int(_version_info[num_i]))
                        self.qrcode.putpixel((num_i % 3 + self.length - 11, num_i // 3), 1 - int(_version_info[num_i]))

            def data_draw():
                return

            self.qrcode = Image.new('1', self.size, 1)
            build_locate_sign()
            build_time_sign()
            build_alignment_sign()
            level_and_mask_draw()
            version_info_draw()
            data_draw()

        def encode():
            def rs(_data):
                return _data

            def mask(_data):
                return _data

            def penalty(_data):
                return 0, 0

            (self.data_matrix, self.mask_id) = penalty(mask(rs(self.encode_data)))

        decide_version(message)
        encode()
        draw()
