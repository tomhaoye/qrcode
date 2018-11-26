#!/usr/bin/python
from PIL import Image
from math import sqrt
from reedsolo import rs_generator_poly, gf_mul
from qsqrcode.constant import mode_map, level_map, format_info_str, version_info_str, alignment_location, num_list, \
    character_amount, ecc_num_version_level_map, mode_indicator_map, character_count_indicator_map, \
    each_version_required_bytes, num_of_error_correction_blocks_2_error_correction_per_blocks, remainder_bits, \
    img_mode_2_color_map


class Qrcode:
    mode = None
    level = None
    qrcode = None
    version = 1
    img_mode = '1'
    data_matrix = None
    mask_id = None
    border = 0
    length = 0
    size = ()
    re_size = None
    gif_qrcode = []
    gif_combine = False
    duration = 100

    def generate(self, path):
        if self.qrcode is None:
            self._matrix_to_img()
        if self.gif_combine:
            self.gif_qrcode[0].save(path, save_all=True, append_images=self.gif_qrcode, duration=self.duration, loop=0)
        else:
            self.qrcode.save(path)
        return

    def resize(self, size):
        self.re_size = size
        if self.qrcode is None:
            self._matrix_to_img()
        if self.gif_combine:
            for qrcode_index in range(len(self.gif_qrcode)):
                self.gif_qrcode[qrcode_index] = self.gif_qrcode[qrcode_index].resize((size, size), Image.NONE)
        else:
            self.qrcode = self.qrcode.resize((size, size), Image.NONE)
        return self

    def set_border(self, border):
        self.border = abs(int(border))
        if self.qrcode is not None and self.re_size is not None:
            new_img = Image.new(self.img_mode, (self.re_size + 2*self.border, self.re_size + 2*self.border), img_mode_2_color_map[self.img_mode][0])
            for x in range(self.re_size):
                for y in range(self.re_size):
                    new_img.putpixel((x + self.border, y + self.border), self.qrcode.getpixel((x, y)))
            self.qrcode = new_img
        return self

    # 由于根据传入图片像素会改变二维码尺寸，如果想添加border请在调用该函数后使用resize调整大小，否则你的电脑风扇可能会很响:)
    def put_img_inside(self, img_path):
        self.img_mode = img_mode = 'RGBA'
        if self.qrcode is None:
            new_matrix = [[None] * self.length for i in range(self.length)]
            for x in range(self.length):
                for y in range(self.length):
                    new_matrix[x][y] = img_mode_2_color_map[img_mode][self.data_matrix[x][y]]
            self._matrix_to_img(img_mode, new_matrix)
        else:
            self.qrcode.convert(img_mode)
        img = Image.open(img_path)
        img_len = img.size[0]
        enlarge_size = img_len * 4
        self.resize(enlarge_size)
        put_begin_xy = (enlarge_size - img_len + self.border) // 2
        for x in range(img_len):
            for y in range(img_len):
                color = img.getpixel((x, y))
                if color[3] > 0:
                    self.qrcode.putpixel((x + put_begin_xy, y + put_begin_xy), color)
        return self

    def paint(self, img, fg_or_bg=0):
        matrix = [[None] * self.length for i in range(self.length)]
        self.img_mode = img_mode = 'RGBA'
        img = Image.open(img)
        img = img.resize(self.size, Image.ANTIALIAS)
        for x in range(self.length):
            for y in range(self.length):
                if fg_or_bg == 0:
                    matrix[x][y] = img.getpixel((x, y)) if img is not None and self.data_matrix[x][y] == 1 else img_mode_2_color_map[img_mode][0]
                else:
                    matrix[x][y] = img.getpixel((x, y)) if img is not None and self.data_matrix[x][y] == 0 else img_mode_2_color_map[img_mode][1]
        self._matrix_to_img(img_mode, matrix)
        return self

    def fill_gif(self, img_path):
        img = Image.open(img_path)
        if img.tile[0][0] != 'gif':
            return self
        self.duration = img.info['duration']
        if img.size[0] != img.size[1]:
            raise Exception('please choose a square picture')
        self.img_mode = img_mode = 'RGB'
        size = img.size[0]
        img_list = []
        new_matrix = [[None] * self.length for i in range(self.length)]
        for x in range(self.length):
            for y in range(self.length):
                new_matrix[x][y] = img_mode_2_color_map[img_mode][self.data_matrix[x][y]]
        while True:
            try:
                seq = img.tell()
                img.seek(seq + 1)
                _gif = img.convert(img_mode)
                self._matrix_to_img(img_mode, new_matrix)
                self.resize(size)
                for x in range(size):
                    for y in range(size):
                        qrcode_xy_value = self.qrcode.getpixel((x, y))
                        gif_xy_value = _gif.getpixel((x, y))
                        self.qrcode.putpixel((x, y), qrcode_xy_value)
                        if gif_xy_value != img_mode_2_color_map[img_mode][0] and qrcode_xy_value != img_mode_2_color_map[img_mode][0]:
                            self.qrcode.putpixel((x, y), gif_xy_value)
                img_list.append(self.qrcode)
            except EOFError:
                break
        self.gif_qrcode = img_list
        self.gif_combine = True
        return self

    def colour(self, fg_color=None, bg_color=None):
        if (fg_color is None or len(fg_color) != 7) and (bg_color is None or len(bg_color) != 7):
            return self
        fg_color = (int(fg_color[1:3], 16), int(fg_color[3:5], 16), int(fg_color[5:7], 16)) if fg_color else None
        bg_color = (int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)) if bg_color else None
        self.img_mode = img_mode = 'RGB'
        matrix = [[None] * self.length for i in range(self.length)]
        for x in range(self.length):
            for y in range(self.length):
                if self.data_matrix[x][y] == 1:
                    matrix[x][y] = fg_color if fg_color is not None else img_mode_2_color_map[img_mode][1]
                else:
                    matrix[x][y] = bg_color if bg_color is not None else img_mode_2_color_map[img_mode][0]
        self._matrix_to_img('RGB', matrix)
        return self

    def _matrix_to_img(self, img_mode='1', matrix=None):
        border = abs(int(self.border))
        size = (self.length + 2 * border, self.length + 2 * border)
        img = Image.new(img_mode, size, img_mode_2_color_map[img_mode][0])
        for x in range(self.length):
            for y in range(self.length):
                img.putpixel((x + border, y + border),
                             (img_mode_2_color_map[img_mode][0] - self.data_matrix[x][y]) if matrix is None else
                             matrix[x][y])
        self.qrcode = img

    def __init__(self, message, level_index='L'):
        self.level = level_map[level_index]
        message = message.encode()

        def decide_version(_message, _level_index):
            if all(chr(i) in num_list for i in _message):
                mode = 'numeric'
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

        def encode(_message):
            def get_data_codewords(__message):
                def numeric_encode(___message):
                    diff_encode_code = ''
                    divided_arr = [___message[i:i + 3] for i in range(0, len(___message), 3)]
                    for _equal_or_less_than_three_digits in divided_arr:
                        respectively_len = 10 - 3 * (3 - len(_equal_or_less_than_three_digits))
                        diff_encode_code += bin(int(_equal_or_less_than_three_digits))[2:].zfill(respectively_len)
                    return diff_encode_code

                def byte_encode(___message):
                    diff_encode_code = ''
                    for b in ___message:
                        diff_encode_code += bin(b)[2:].zfill(8)
                    return diff_encode_code

                mode_encode = {
                    'numeric': numeric_encode,
                    'byte': byte_encode,
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
