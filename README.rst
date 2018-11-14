================
QRCode generator
================

install::

    pip install qs-qrcode

usage
=====

use in python:

.. code:: python

    from qsqrcode.qrcode import Qrcode

    qr = Qrcode('test it')
    qr.generate('testpic/test.png')

more usage
----------

.. code:: python

    from qsqrcode.qrcode import Qrcode

    # Qrcode 的第二个参数，L ≈ 7%容错，M ≈ 15%容错，Q ≈ 25%容错，H ≈ 30%容错
    Qrcode('test', 'L').generate('testpic/test7.png')
    Qrcode('test', 'M').generate('testpic/test8.png')
    Qrcode('test', 'Q').generate('testpic/test9.png')
    Qrcode('test', 'H').generate('testpic/testA.png')

    Qrcode('填充颜色', 'H').colour('#1294B8').resize(250).generate('testpic/test1.png')

    Qrcode('填充图片', 'H').paint('pic/testbg.jpg').resize(250).generate('testpic/test2.png')

    Qrcode('再看看如何加border', 'H').paint('pic/test.jpg').resize(230).set_border(10).generate('testpic/test3.png')

    Qrcode('测试二维码中间加入图片', 'H').put_img_inside('pic/mystic.png').resize(375).generate('testpic/test4.png')

    Qrcode('gif试试看，但效果并不好看，而且暂不支持set_border', 'H').fill_gif('pic/pla.gif').resize(250).generate('testpic/testD.gif')

