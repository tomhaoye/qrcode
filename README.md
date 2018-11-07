# 二维码生成器（QRCode generator）

可用于生成普通黑白二维码、彩色二维码、带背景图片的二维码，在微信扫码等主流扫码器中支持所有语言的识别。

> zwf

## 书签

 - [书签](#书签)
 - [环境](#环境)
 - [依赖](#依赖)
 - [安装](#安装)
 - [使用](#使用)
 - [示例](#示例)
 
 ## 环境
 
  - Python3.x
    - Windows
    - Linux
    - MacOS 
 
 ## 依赖
 
 - Pillow
 - reedsolo
 
 ## 安装
 
 > 还没能直接安装
 
 ## 使用
 - 命令行
```bash
python test.py 
```
 - 文件引入
```python
from qsqrcode.qrcode import Qrcode

qr = Qrcode('测试一下吧', 'H')
qr.paint('pic/test.jpg').generate('testpic/test.png')
```
 
 
 ## 示例
 [](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test.png)
 [](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test1.png)
 