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

    qr = Qrcode('填充图片', 'H')
    qr.paint('pic/testbg.jpg').resize(250).generate('testpic/test1.png')

    qr = Qrcode('填充颜色', 'H')
    qr.colour('#1294B8').resize(250).generate('testpic/test2.png')

    qr = Qrcode('再看看如何加border', 'H')
    qr.paint('pic/test.jpg').resize(230).set_border(10).generate('testpic/test3.png')
