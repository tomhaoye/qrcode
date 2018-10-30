#!/usr/bin/python
from PIL import Image
from math import sqrt
from .constant import mode_map, level_map, format_info_str, version_info_str, alignment_location, num_list, \
    alphanum_list, character_amount, ecc_num_version_level_map


class Qrcode:
    mode = None
    level = None
    qrcode = None
    version = 1
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

    def __init__(self, message, level_index='L'):
        self.level = level_map[level_index]

        def decide_version(_message, _level_index):
            if all(i in num_list for i in _message):
                mode = 'numeric'
            elif all(i in alphanum_list for i in _message):
                mode = 'alphanumeric'
            elif all(ord(i) in range(256) for i in _message):
                mode = 'byte'
            else:
                mode = 'kanji'
            for each_version in range(40):
                if character_amount[_level_index][each_version][mode_map[mode]] > len(_message):
                    self.version = each_version + 1 if each_version + 1 > self.version else self.version
                    break
            self.length = 21 + 4 * (self.version - 1)
            self.size = (self.length, self.length)
            self.mode = mode
            print(self.version)

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
                        format_i + 1 if format_i < 8 else self.length - 7 + (format_i - 8)), 8), 1 - int(
                        format_info_str[self.level][self.mask_id][format_i]))
                    self.qrcode.putpixel((8, format_i if format_i < 6 else (
                        format_i + 1 if format_i < 8 else self.length - 7 + (format_i - 8))),
                                         1 - int(format_info_str[self.level][self.mask_id][14 - format_i]))
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
            data_draw()
            level_and_mask_draw()
            version_info_draw()

        def encode():
            def numeric_encode(_message):
                code = []
                divided_arr = [_message[i:i + 3] for i in range(0, len(_message), 3)]
                for _equal_or_less_than_three_digits in divided_arr:
                    respectively_len = 10 - 3 * (3 - len(_equal_or_less_than_three_digits))
                    code.append(bin(int(_equal_or_less_than_three_digits))[2:].zfill(respectively_len))
                return code

            def alphanumeric_encode(_message):
                code = []
                trans_list = [alphanum_list.index(s) for s in _message]
                for i in range(1, len(trans_list), 2):
                    code.append(bin(trans_list[i - 1] * 45 + trans_list[i])[2:].zfill(11))
                code if i == len(trans_list) - 1 else code.append(bin(trans_list[-1])[2:].zfill(6))
                return code

            def byte_encode(_message):
                code = []
                for b in _message:
                    code.append(bin(ord(b.encode('iso-8859-1')))[2:].zfill(8))
                return code

            def kanji_encode(_message):
                return []

            def rs_encode():
                ecc_num = ecc_num_version_level_map[self.version][self.level]

            def mask():
                return

            def penalty():
                return 0, 0

            rs_encode()
            mask()
            (self.data_matrix, self.mask_id) = penalty()

        decide_version(message, level_index)
        encode()
        draw()
