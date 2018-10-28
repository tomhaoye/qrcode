#!/usr/bin/python
from PIL import Image


class Qrcode:
    qrcode = None

    def resize(self, size):
        return self.qrcode

    def generate(self, path):
        self.qrcode.save(path)
        return

    def __init__(self, message):
        def decide_version(message):
            return version

        def draw(size, data):
            def build_locate_sign():
                return

            def build_time_sign():
                return

            def draw_data():
                return

            return qrcode

        def encode(message):
            def rs():
                return

            def mask():
                return

            def penalty():
                return

            return qrcode

        version = decide_version(message)
        encode_data = encode(message)
        self.qrcode = draw(version, encode_data)
