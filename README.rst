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
    qr = Qrcode('test it', 'H')
    qr.paint('pic/testbg.jpg').resize(250).generate('testpic/test1.png')
    qr.colour((199, 29, 69)).resize(250).generate('testpic/test2.png')
