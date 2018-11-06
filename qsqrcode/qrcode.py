#!/usr/bin/python
from PIL import Image
from math import sqrt
from reedsolo import rs_generator_poly, gf_mul
from .constant import mode_map, level_map, format_info_str, version_info_str, alignment_location, num_list, \
    alphanum_list, character_amount, ecc_num_version_level_map, mode_indicator_map, character_count_indicator_map, \
    each_version_required_bytes, num_of_error_correction_blocks_2_error_correction_per_blocks, remainder_bits


class Qrcode:
    py_version = 3
    mode = None
    level = None
    qrcode = None
    version = 1
    data_matrix = None
    mask_id = None
    length = 0
    size = ()

    def resize(self, size):
        self.qrcode = self.qrcode.resize((size, size), Image.ANTIALIAS)
        return self

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
            elif all(ord(i) in range(0x4E00, 0x9FA6) for i in _message):
                mode = 'zh_CN'
            elif any(ord(i) in range(0x3040, 0x3100) for i in _message):
                mode = 'kanji'
            else:
                mode = 'byte'
            for each_version in range(40):
                if character_amount[_level_index][each_version][mode_map[mode]] > len(_message):
                    self.version = each_version + 1 if each_version + 1 > self.version else self.version
                    break
            self.length = 21 + 4 * (self.version - 1)
            self.size = (self.length, self.length)
            self.mode = mode

        def build_matrix(encode_data):
            def build_locate_sign():
                for i in range(8):
                    for j in range(8):
                        if i in (0, 6):
                            self.data_matrix[i][j] = self.data_matrix[-i - 1][j] = self.data_matrix[i][
                                -j - 1] = 0 if j == 7 else 1
                        elif i in (1, 5):
                            self.data_matrix[i][j] = self.data_matrix[-i - 1][j] = self.data_matrix[i][
                                -j - 1] = 1 if j in (0, 6) else 0
                        elif i == 7:
                            self.data_matrix[i][j] = self.data_matrix[-i - 1][j] = self.data_matrix[i][-j - 1] = 0
                        else:
                            self.data_matrix[i][j] = self.data_matrix[-i - 1][j] = self.data_matrix[i][
                                -j - 1] = 0 if j in (1, 5, 7) else 1

            def build_time_sign():
                for i in range(self.length):
                    self.data_matrix[i][6] = self.data_matrix[6][i] = 1 if i % 2 == 0 else 0

            def build_dark_sign():
                for j in range(8):
                    self.data_matrix[8][j] = self.data_matrix[8][-j - 1] = self.data_matrix[j][8] = \
                        self.data_matrix[-j - 1][8] = 0
                self.data_matrix[8][8] = 0
                self.data_matrix[8][6] = self.data_matrix[6][8] = self.data_matrix[8][-8] = 1
                if self.version > 6:
                    for i in range(6):
                        for j in (-9, -10, -11):
                            self.data_matrix[i][j] = self.data_matrix[j][i] = 0

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
                        for x_offset in range(-2, 3):
                            for y_offset in range(-2, 3):
                                self.data_matrix[point_matrix[index][0] + x_offset][point_matrix[index][1] + y_offset] \
                                    = 1 if x_offset % 2 == 0 and y_offset % 2 == 0 or abs(x_offset) + abs(
                                    y_offset) == 3 else 0

            def level_and_mask_build(_mask_id):
                for format_i in range(len(format_info_str[self.level][_mask_id])):
                    self.data_matrix[format_i if format_i < 6 else (
                        format_i + 1 if format_i < 8 else self.length - 7 + (format_i - 8))][8] = int(
                        format_info_str[self.level][_mask_id][format_i])
                    self.data_matrix[8][format_i if format_i < 6 else (
                        format_i + 1 if format_i < 8 else self.length - 7 + (format_i - 8))] = int(
                        format_info_str[self.level][_mask_id][14 - format_i])
                self.data_matrix[self.length - 8][8] = int(format_info_str[self.level][_mask_id][7])

            def build_version_info():
                if self.version > 6:
                    _version_info = version_info_str[self.version][::-1]
                    for num_i in range(len(_version_info)):
                        self.data_matrix[num_i // 3][num_i % 3 + self.length - 11] = int(_version_info[num_i])
                        self.data_matrix[num_i % 3 + self.length - 11][num_i // 3] = int(_version_info[num_i])

            def data_build(_encode_data):
                up = True
                bit = (int(i) for i in _encode_data)
                for _block_end_x in range(self.length - 1, 0, -2):
                    _block_end_x = _block_end_x if _block_end_x > 6 else _block_end_x - 1
                    for y in range(self.length - 1, -1, -1) if up else range(self.length):
                        for x in (_block_end_x, _block_end_x - 1):
                            if self.data_matrix[x][y] is None:
                                self.data_matrix[x][y] = next(bit, 0)
                    up = not up

            def mask():
                def mask_template(col, row, _mask_id):
                    if _mask_id == 0:
                        return (col + row) % 2 == 0
                    elif _mask_id == 1:
                        return row % 2 == 0
                    elif _mask_id == 2:
                        return col % 3 == 0
                    elif _mask_id == 3:
                        return (row + col) % 3 == 0
                    elif _mask_id == 4:
                        return (row // 2 + col // 3) % 2 == 0
                    elif _mask_id == 5:
                        return ((row * col) % 2) + ((row * col) % 3) == 0
                    elif _mask_id == 6:
                        return (((row * col) % 2) + ((row * col) % 3)) % 2 == 0
                    elif _mask_id == 7:
                        return (((row + col) % 2) + ((row * col) % 3)) % 2 == 0
                    else:
                        return (col + row) % 2 == 0

                def penalty(__matrix):
                    def cal_n3(___matrix):
                        _count = 0
                        check_word = ('00001011101', '10111010000')
                        for row in ___matrix:
                            row_str = ''.join(str(s) for s in row)
                            begin = 0
                            while begin < len(row_str) and check_word[0] in row_str[begin:]:
                                begin += row_str[begin:].index(check_word[0]) + len(check_word[0])
                                _count += 1
                            begin = 0
                            while begin < len(row_str) and check_word[1] in row_str[begin:]:
                                begin += row_str[begin:].index(check_word[1]) + len(check_word[1])
                                _count += 1
                        return _count

                    def get_sum(___matrix):
                        num = 0
                        for v in ___matrix:
                            if v is list:
                                num += get_sum(v)
                        return num + sum(map(sum, ___matrix))

                    n1 = 0
                    n2 = 0
                    n3 = 0
                    n4 = 0
                    # N1寻找连续同色块which >= 5
                    for reverse in range(0, 2):
                        for j in range(reverse, self.length):
                            count = 1
                            adj = False
                            for i in range(1 - reverse, self.length):
                                if __matrix[j][i] == __matrix[j][i - 1]:
                                    count += 1
                                else:
                                    count = 1
                                    adj = False
                                if count >= 5:
                                    if not adj:
                                        adj = True
                                        n1 += 3
                                    else:
                                        n1 += 1
                    # N2寻找m * n的同色块
                    count = 0
                    for j in range(self.length):
                        for i in range(self.length):
                            if __matrix[j][i] == __matrix[j - 1][i] and __matrix[j][i] == \
                                    __matrix[j][i - 1] and __matrix[j][i] == __matrix[j - 1][i - 1]:
                                count += 1
                    n2 += 3 * count
                    # N3寻找连续四空色块0000连接1011101色块
                    # 一个方向寻找 + 另一个方向(矩阵转置)
                    transposition_matrix = list(zip(*__matrix))
                    n3 += 40 * cal_n3(__matrix) + cal_n3(transposition_matrix)
                    # N4计算黑色块占比
                    dark = get_sum(__matrix)
                    percent = dark // pow(self.length, 2) * 100
                    pre = percent - percent % 5
                    nex = percent + 5 - percent % 5
                    n4 = min(abs(pre - 50) / 5, abs(nex - 50) / 5) * 10
                    return n1 + n2 + n3 + n4

                penalty_result = []
                _matrix_with_mask = []
                for mask_id in range(8):
                    level_and_mask_build(mask_id)
                    _matrix = [[None] * self.length for _i in range(self.length)]
                    for x in range(self.length):
                        for y in range(self.length):
                            if self.data_matrix[x][y] is not None:
                                _matrix[x][y] = self.data_matrix[x][y] ^ mask_template(x, y, mask_id)
                    penalty_result.append(penalty(_matrix))
                    _matrix_with_mask.append(_matrix)
                _best_mask_id = penalty_result.index(min(penalty_result))
                self.data_matrix = _matrix_with_mask[_best_mask_id]
                return _best_mask_id

            def build_fix_sign():
                build_time_sign()
                build_dark_sign()
                build_locate_sign()
                build_alignment_sign()
                build_version_info()

            self.data_matrix = [[None] * self.length for i in range(self.length)]
            build_fix_sign()
            data_build(encode_data)
            self.mask_id = mask()
            build_fix_sign()
            level_and_mask_build(self.mask_id)

        def draw():
            self.qrcode = Image.new('1', self.size, 1)
            for x in range(self.length):
                for y in range(self.length):
                    self.qrcode.putpixel((x, y), 0 if self.data_matrix[x][y] else 1)

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
                    if self.py_version > 3:
                        ___message = ___message.encode()
                        for ord_b in ___message:
                            diff_encode_code += bin(ord_b)[2:].zfill(8)
                    else:
                        for b in ___message:
                            diff_encode_code += bin(ord(b))[2:].zfill(8)
                    return diff_encode_code

                def kanji_encode(___message):
                    code = ''
                    for i in ___message:
                        data = i.encode('cp932')
                        value = data[0] * 16 * 16 + data[1]
                        if value in range(0x8140, 0x9FFD):
                            value = value - 0x8140
                            length = len(bin(value))
                            high = bin(value)[2:length - 8]
                            low = bin(value)[-8:]
                            c = bin(int(high, 2) * 0xC0 + int(low, 2))[2:]
                            c = '0' * (13 - len(c)) + c
                            code += c
                        elif value in range(0xE040, 0xEBC0):
                            value = value - 0xC140
                            length = len(bin(value))
                            high = bin(value)[2:length - 8]
                            low = bin(value)[-8:]
                            c = bin(int(high, 2) * 0xC0 + int(low, 2))[2:]
                            c = '0' * (13 - len(c)) + c
                            code += c
                    return code

                def zh_cn_encode(___message):
                    code = ''
                    for i in ___message:
                        data = i.encode('gb2312')
                        value = data[0] * 16 * 16 + data[1]
                        length = len(bin(value))
                        high = int(bin(value)[2:length - 8], 2)
                        low = int(bin(value)[-8:], 2)
                        if high in range(0xA1, 0xAB) and low in range(0xA1, 0xFF):
                            c = bin((high - 0xA1) * 0x60 + low - 0xA1)[2:]
                            c = '0' * (13 - len(c)) + c
                            code += c
                        elif high in range(0xB0, 0xFB) and low in range(0xA1, 0xFF):
                            c = bin((high - 0xA6) * 0x60 + low - 0xA1)[2:]
                            c = '0' * (13 - len(c)) + c
                            code += c
                    return code

                mode_encode = {
                    'numeric': numeric_encode,
                    'alphanumeric': alphanumeric_encode,
                    'byte': byte_encode,
                    'kanji': kanji_encode,
                    'zh_CN': zh_cn_encode,
                }
                incomplete_codewords = mode_indicator_map[self.mode] + bin(len(__message))[2:].zfill(
                    character_count_indicator_map[self.version][mode_map[self.mode]]) + mode_encode[self.mode](_message)
                distance_to_8_multiple = 8 - (len(incomplete_codewords) % 8)
                incomplete_codewords += '0' * distance_to_8_multiple

                codewords = incomplete_codewords
                bytes_need = 8 * each_version_required_bytes[self.version][self.level]
                while len(codewords) < bytes_need:
                    codewords += '1110110000010001' if bytes_need - len(codewords) >= 16 else '11101100'
                _data_codewords = [int(codewords[i:i + 8], 2) for i in range(len(codewords)) if not i % 8]
                return _data_codewords

            def rs_encode(_data_codewords):
                _encode_data, data_block, i = '', [], 0
                block_codecount = num_of_error_correction_blocks_2_error_correction_per_blocks[self.version][self.level]
                for group1 in range(block_codecount[0]):
                    data_block.append(_data_codewords[i:i + block_codecount[1]])
                    i += block_codecount[1]
                for group2 in range(block_codecount[2]):
                    data_block.append(_data_codewords[i:i + block_codecount[3]])
                    i += block_codecount[3]

                nsym = ecc_num_version_level_map[self.version][self.level]
                gen = rs_generator_poly(nsym)
                ecc_num = len(gen) - 1
                _ecc_data = []
                for block in data_block:
                    _data_block_get_ecc_block = block + [0] * ecc_num
                    for i in range(len(block)):
                        coef = _data_block_get_ecc_block[i]
                        if coef != 0:
                            for j in range(ecc_num + 1):
                                _data_block_get_ecc_block[i + j] ^= gf_mul(gen[j], coef)
                    _ecc_data.append(_data_block_get_ecc_block[len(block):])

                _all_block_data = ''.join(bin(dec)[2:].zfill(8) for block in zip(*data_block) for dec in block)
                # 突出部分补全
                for block in data_block:
                    if len(block) == block_codecount[3]:
                        _all_block_data += bin(block[block_codecount[3] - 1])[2:].zfill(8)
                _all_ecc_data = ''.join(bin(dec)[2:].zfill(8) for block in zip(*_ecc_data) for dec in block)
                return _all_block_data + _all_ecc_data + '0' * remainder_bits[self.version]

            data_codewords = get_data_codewords(_message)
            return rs_encode(data_codewords)

        decide_version(message, level_index)
        build_matrix(encode(message))
        draw()
