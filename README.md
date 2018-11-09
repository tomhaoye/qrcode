# 二维码生成器（QRCode generator）

可用于生成普通黑白二维码、彩色二维码、带背景图片的二维码，在微信扫码等主流扫码器中支持所有语言的识别。

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
 
 ```bash
 sudo pip install -r requirements.txt
 ```
 
 ## 安装
 
 ```bash
sudo pip install qs-qrcode
```
 
 ## 使用
 - 命令行
 > 暂时可以通过修改`test.py`文件进行生成，如果想要支持命令行生成，请耐心等待`:)`
```bash
python test.py 
```
 - 文件引入
```python
from qsqrcode.qrcode import Qrcode

# 最直接的使用
Qrcode('测试一下吧').generate('testpic/test0.png')

# 规定二维码大小
Qrcode('测试一下吧').resize(250).generate('testpic/test1.png')

# 给二维码添加border
Qrcode('测试一下吧').set_border(20).generate('testpic/test2.png')

# 给二维码填充图片
Qrcode('测试一下吧').paint('pic/test.jpg').generate('testpic/test3.png')

# 给二维码填充颜色
Qrcode('测试一下吧').colour('#22AA66').generate('testpic/test4.png')

# 一顿骚操作
Qrcode('测试一下吧').colour('#22AA66').resize(250).set_border(10).generate('testpic/test5.png')
Qrcode('测试一下吧').paint('pic/test.jpg').resize(250).set_border(10).generate('testpic/test6.png')

```
 
 
 ## 示例
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test4.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test5.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test2.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test3.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test0.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test1.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test6.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test7.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test8.png)