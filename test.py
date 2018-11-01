from qsqrcode.qrcode import Qrcode

qr = Qrcode('hello', 'M')
qr.generate('test.png')
