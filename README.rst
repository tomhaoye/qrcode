二维码生成器（QRCode generator）
================================

安装::

    pip install qs-qrcode

使用方法
=======

在python文件中引入使用:

.. code:: python

    from qsqrcode.qrcode import Qrcode
    qr = Qrcode('测试一下吧')
    qr.generate('testpic/test.png')

更深入的用法
-----------

.. code:: python

    from qsqrcode.qrcode import Qrcode
    qr = Qrcode('测试一下吧', 'H')
    qr.paint('pic/testbg.jpg').resize(250).generate('testpic/test1.png')
    qr.colour((199, 29, 69)).resize(250).generate('testpic/test2.png')

``Qrcode``的第二个参数为纠错等级，可传以下这四种值：

``L`` (默认值)
    7%的错误可被纠正
``M``
    15%的错误可被纠正
``Q``
    25%的错误可被纠正
``H``.
    30%的错误可被纠正

``colour``函数第一个参数为修改二维码填充颜色，第二个参数为修改二维码背景颜色
``paint``函数第一个参数为需要填充的照片路径，第二个参数为作为背景或是色块被填充
``resize``函数需要传入图片长/宽度
``generate``函数需要传入保存的路径
