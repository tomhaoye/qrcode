from qsqrcode.qrcode import Qrcode

qr = Qrcode('test', 'L')
qr.generate('test.png')
