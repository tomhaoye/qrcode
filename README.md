# 二维码生成器（QRCode generator）

<p>
<a href="#"><img src="https://img.shields.io/github/languages/top/tomhaoye/qrcode" alt="lang"></a>
<a href="#"><img src="https://img.shields.io/badge/Python->=3-green.svg" alt="limit"></a>
<a href="#"><img src="https://img.shields.io/github/languages/code-size/tomhaoye/qrcode" alt="size"></a>
<a href="#"><img src="https://img.shields.io/github/last-commit/tomhaoye/qrcode" alt="last"></a>
<a href="#"><img src="https://img.shields.io/pypi/dm/qs-qrcode" alt="download"></a>
<a href="#"><img src="https://img.shields.io/github/license/tomhaoye/qrcode" alt="license"></a>
</p>

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
# 如果使用pip安装扩展可免去该步骤
sudo pip install -r requirements.txt
```
 
 ## 安装
 
```bash
sudo pip install qs-qrcode
```
 
 ## 使用
 - 命令行
>使用`pip`安装该扩展高于或等于`1.1`版本
```bash
qsqrcode -l H -m 唱歌不如跳舞 -s 400 -b 20 -c #569932
```
>如果你只克隆了项目而没有使用`pip`安装扩展
```bash
python qsqrcode.py -l H -m 唱歌不如跳舞 -s 400 -b 20 -c #569932
```
>更多用法及解释
```bash
qsqrcode -h
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
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/testF.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test0.png)
 ![](https://raw.githubusercontent.com/tomhaoye/qrcode/master/testpic/test1.png)