#!/usr/bin/python
from PIL import Image
from math import sqrt
from .constant import mode_map, level_map, format_info_str, version_info_str, alignment_location, num_list, \
    alphanum_list, character_amount, ecc_num_version_level_map, mode_indicator_map, character_count_indicator_map, \
    each_version_required_bytes


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

        def encode(_message):
            def get_data_codewords(__message):
                def numeric_encode(___message):
                    diff_encode_code = ''
                    divided_arr = [___message[i:i + 3] for i in range(0, len(___message), 3)]
                    for _equal_or_less_than_three_digits in divided_arr:
                        respectively_len = 10 - 3 * (3 - len(_equal_or_less_than_three_digits))
                        diff_encode_code += bin(int(_equal_or_less_than_three_digits))[2:].zfill(respectively_len)
                    return diff_encode_code

                def alphanumeric_encode(___message):
                    diff_encode_code = ''
                    trans_list = [alphanum_list.index(s) for s in ___message]
                    for i in range(1, len(trans_list), 2):
                        diff_encode_code += bin(trans_list[i - 1] * 45 + trans_list[i])[2:].zfill(11)
                    return diff_encode_code if i == len(trans_list) - 1 else diff_encode_code + bin(trans_list[-1])[
                                                                                                2:].zfill(6)

                def byte_encode(___message):
                    diff_encode_code = ''
                    for b in ___message:
                        diff_encode_code += bin(ord(b.encode('iso-8859-1')))[2:].zfill(8)
                    return diff_encode_code

                def kanji_encode(___message):
                    return []

                incomplete_codewords = mode_indicator_map[self.mode] + (
                    numeric_encode(__message) if self.mode == 'numeric' else (
                        alphanumeric_encode(__message) if self.mode == 'alphanumeric' else (
                            byte_encode(__message) if self.mode == 'byte' else kanji_encode(__message)))) + bin(
                    len(__message))[2:].zfill(character_count_indicator_map[self.version][mode_map[self.mode]])
                distance_to_8_multiple = 8 - (len(incomplete_codewords) % 8)
                incomplete_codewords += '0' * distance_to_8_multiple

                codewords = incomplete_codewords
                bytes_need = 8 * each_version_required_bytes[self.version][self.level]
                while len(codewords) < bytes_need:
                    codewords += '1110110000010001' if bytes_need - len(codewords) >= 16 else '11101100'
                return codewords

            def rs_encode(_data_codewords):
                ecc_num = ecc_num_version_level_map[self.version][self.level]

            def mask():
                return

            def penalty():
                return 0, 0

            data_codewords = get_data_codewords(_message)
            rs_encode(data_codewords)
            mask()
            (self.data_matrix, self.mask_id) = penalty()

        decide_version(message, level_index)
        encode(message)
        draw()
