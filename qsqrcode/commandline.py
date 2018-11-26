import sys
import getopt
from qsqrcode.qrcode import Qrcode


def main():
    try:
        opts, left_args = getopt.getopt(sys.argv[1:], "b:c:hi:l:m:p:s:",
                                        ["border=", "color=", "inside=", "level=", "message=", "path=", "size="])
    except getopt.GetoptError:
        print('You should use `qsqrcode -h` to get the usage.')
        sys.exit(2)

    size = None
    color = None
    border = None
    img_inside = None
    ecc_level = 'L'
    message = 'nothing input'
    save_path = 'default.png'
    if len(opts) == 0:
        print("You input nothing and it will generate a default.png in your current dir!\n"
              "Perhaps you can use `qsqrcode -h` to get the usage.")
    for opt, arg in opts:
        if opt == '-h':
            print('Mandatory arguments to long options are mandatory for short options too\n'
                  '-l, --level <ecc_level>      choose a ecc level if you know\n'
                  '-m, --message <message>      input the message you want to encode\n'
                  '-p, --path <save_path>       input a dir with the name for the qrcode\n'
                  '-s, --size <qrcode_size>     if you input 300, you will get a 300*300 qrcode\n'
                  '-b, --border <border_size>   you will get a 320*320 qrcode if you input -b 10 -s 300\n'
                  '-c, --color <qrcode_color>   please input a hexadecimal number for the color(like #882566)\n'
                  '-i, --inside <img_inside>    input a img path which you want to put it in the middle of qrcode')
            sys.exit()
        if opt in ('-m', '--message'):
            message = arg
        if opt in ('-l', '--level'):
            ecc_level = arg
        if opt in ('-p', '--path'):
            save_path = arg
        if opt in ('-s', '--size'):
            size = int(arg)
        if opt in ('-b', '--border'):
            border = int(arg)
        if opt in ('-c', '--color'):
            color = arg
        if opt in ('-i', '--inside'):
            img_inside = arg

    qrcode = Qrcode(message, ecc_level)
    if color:
        qrcode.colour(color)
    elif img_inside:
        qrcode.put_img_inside(img_inside)
    if size:
        qrcode.resize(size)
    if border:
        qrcode.set_border(border)
    qrcode.generate(save_path)
