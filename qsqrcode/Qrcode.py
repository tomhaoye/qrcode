#!/usr/bin/python
from PIL import Image


class Qrcode:
    qrcode = None

    def resize(self, size):
        self.qrcode.resize((size, size), Image.ANTIALIAS)
        return self.qrcode

    def generate(self, path):
        self.qrcode.save(path)
        return

    def __init__(self, message):
        def decide_version(message):
            _version = 0
            return _version

        def draw(size, data_matrix):
            def build_locate_sign():
                return

            def build_time_sign():
                return

            def data_to_draw(_data):
                return

            self.qrcode = Image.new('1', (size, size), 1)
            build_locate_sign()
            build_time_sign()
            data_to_draw(data_matrix)

        def encode(data_to_encode):
            def rs(_data):
                return _data

            def mask(_data):
                return _data

            def penalty(_data):
                return _data

            data_matrix = penalty(mask(rs(data_to_encode)))
            return data_matrix

        version = decide_version(message)
        encode_data = encode(message)
        draw(version, encode_data)
