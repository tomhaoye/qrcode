#!/usr/bin/python
from PIL import Image


class Qrcode:
    qrcode = None
    version = None
    encode_data = None
    data_matrix = None
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
            self.size = (21, 21)

        def draw():
            def build_locate_sign():
                return

            def build_time_sign():
                return

            def build_version_sign():
                return

            def data_to_draw():
                return

            self.qrcode = Image.new('1', self.size, 1)
            build_locate_sign()
            build_time_sign()
            build_version_sign()
            data_to_draw()

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
