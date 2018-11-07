from qsqrcode.qrcode import Qrcode

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.paint('pic/test.jpg').resize(250).generate('testpic/test0.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.paint('pic/test.jpg', 1).resize(250).generate('testpic/test1.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.colour((199, 29, 69)).resize(250).generate('testpic/test2.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.colour(None, (199, 29, 69)).resize(250).generate('testpic/test3.png')

qr = Qrcode('https://blog.aikeji.online/2018/10/16/%E4%BA%8C%E7%BB%B4%E7%A0%81%E7%94%9F%E6%88%90%E5%8E%9F%E7%90%86%E5%8F%8A%E7%BC%96%E7%A0%81%E5%AE%9E%E7%8E%B0/', 'H')
qr.resize(250).generate('testpic/test4.png')

qr = Qrcode('日本では「ノストラダムスの大予言」の名で知られる詩集を著した。彼の予言は、現在に至るまで多くの信奉者を生み出し、様々な論争を引き起こし다양한 사전 콘텐츠 제공, 발음듣기, 중국어 필기인식기, 보조사전, 내가 찾은 단어 제공', 'H')
qr.resize(250).generate('testpic/test5.png')

