from qsqrcode.qrcode import Qrcode

qr = Qrcode('test qrcode', 'M')
qr.generate('test.png')
