#!/usr/bin/python
from PIL import Image
from .constant import alignment_location


class Qrcode:
    qrcode = None
    version = None
    encode_data = None
    data_matrix = None
    length = 0
    size = ()

    def resize(self, size):
        self.qrcode.resize((size, size), Image.ANTIALIAS)
        return self.qrcode

    def generate(self, path):
        self.qrcode.save(path)
        return

    def __init__(self, message):
        def decide_version(message):
            self.version = 1
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
                if alignment_location[self.version]:
                    return

            def version_info_draw():
                return

            def data_draw():
                return

            self.qrcode = Image.new('1', self.size, 1)
            build_locate_sign()
            build_time_sign()
            build_alignment_sign()
            version_info_draw()
            data_draw()

        def encode():
            def rs(_data):
                return _data

            def mask(_data):
                return _data

            def penalty(_data):
                return _data

            self.data_matrix = penalty(mask(rs(self.encode_data)))

        decide_version(message)
        encode()
        draw()
