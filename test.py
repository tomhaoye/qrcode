from qsqrcode.qrcode import Qrcode

qr = Qrcode('test qrcode', 'L')
qr.generate('test.png')
