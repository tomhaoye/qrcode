# -*- coding: utf-8 -*-
from qsqrcode.qrcode import Qrcode

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.paint('pic/test.jpg').resize(250).generate('testpic/test0.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.paint('pic/testbg.jpg', 1).resize(250).generate('testpic/test1.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.colour('#882566').resize(250).generate('testpic/test2.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.colour(None, '#1294B8').resize(250).generate('testpic/test3.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.resize(250).generate('testpic/test4.png')

qr = Qrcode('日本では「ノストラダムスの大予言」の名で知られる詩集を著した。彼の予言は、現在に至るまで多くの信奉者を生み出し、様々な論争を引き起こし다양한 사전 콘텐츠 제공, 발음듣기, 중국어 필기인식기, 보조사전, 내가 찾은 단어 제공', 'H')
qr.resize(250).generate('testpic/test5.png')

Qrcode('测试一下set_border后resize', 'H').set_border(2).resize(250).generate('testpic/test6.png')

Qrcode('测试一下resize后set_border', 'H').resize(230).set_border(10).generate('testpic/test7.png')

Qrcode('再看看如何', 'H').paint('pic/test.jpg').resize(230).set_border(10).generate('testpic/test8.png')

# 由于根据传入图片像素会改变二维码尺寸，如果想添加border请在调用该函数后使用resize调整大小，否则你的电脑风扇可能会很响:)
Qrcode('测试二维码中间加入图片', 'H').put_img_inside('pic/test_inside.png').resize(180).generate('testpic/test9.png')

Qrcode('测试图片填充二维码中间加入图片', 'H').paint('pic/test.jpg').put_img_inside('pic/test_inside.png').resize(180).generate('testpic/testA.png')

Qrcode('测试颜色填充二维码中间加入图片', 'H').colour('#882566').put_img_inside('pic/test_inside.png').resize(180).generate('testpic/testB.png')

Qrcode('测试二维码中间加入图片后添加border', 'H').put_img_inside('pic/test_inside.png').resize(160).set_border(10).generate('testpic/testC.png')

Qrcode('gif试试看，但效果并不好看，而且暂不支持set_border', 'H').fill_gif('pic/pla.gif').resize(250).generate('testpic/testD.gif')
Qrcode('gif试试看，但效果并不好看，而且暂不支持set_border', 'H').fill_gif('pic/bounce.gif').resize(250).generate('testpic/testE.gif')

Qrcode('插入图片的艺术化二维码', 'Q').resize(250).combine('pic/test1.jpg').generate('testpic/testF.png')