from qsqrcode.qrcode import Qrcode

qr = Qrcode('http://blog.aikeji.online', 'Q')
qr.generate('test.png')
