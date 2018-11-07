from qsqrcode.qrcode import Qrcode

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.paint('pic/test.jpg').generate('testpic/test1.png')
