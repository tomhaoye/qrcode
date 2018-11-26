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
```bash
python qsqrcode.py -l H -w 编码内容 -p /home/qqq/pic.png
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

# 差点忘了 Qrcode 的第二个参数，L ≈ 7%容错，M ≈ 15%容错，Q ≈ 25%容错，H ≈ 30%容错
Qrcode('测试一下吧', 'L').generate('testpic/test7.png')
Qrcode('测试一下吧', 'M').generate('testpic/test8.png')
Qrcode('测试一下吧', 'Q').generate('testpic/test9.png')
Qrcode('测试一下吧', 'H').generate('testpic/testA.png')

# v0.9 添加二维码中间加入图片功能
Qrcode('测试二维码中间加入图片', 'H').put_img_inside('pic/mystic.png').resize(375).generate('testpic/testB.png')
Qrcode('测试图片填充二维码中间加入图片', 'H').paint('pic/test.jpg').put_img_inside('pic/mystic.png').resize(375).generate('testpic/testC.png')
Qrcode('测试颜色填充二维码中间加入图片', 'H').colour('#882566').put_img_inside('pic/mystic.png').resize(375).generate('testpic/testD.png')
Qrcode('测试二维码中间加入图片后添加border', 'H').put_img_inside('pic/mystic.png').resize(335).set_border(20).generate('testpic/testE.png')

# 还有其他一些操作大家可以自行挖掘:)

```
 
 
 ## 示例
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/testD.gif)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test5.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test2.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test3.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test0.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test1.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test6.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test7.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test8.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test9.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/testA.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/testB.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/testC.png)