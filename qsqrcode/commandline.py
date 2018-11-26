import sys
import getopt
from qsqrcode.qrcode import Qrcode


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:w:p:", ["level=", "word=", "path="])
    except getopt.GetoptError:
        print('qsqrcode.py -l <ecc_level> -w <word>')
        sys.exit(2)

    ecc_level = 'L'
    word = 'nothing input'
    save_path = 'default.png'
    for opt, arg in opts:
        if opt == '-h':
            print('qsqrcode.py -l <ecc_level> -w <word>')
            sys.exit()
        if opt in ('-w', '--word'):
            word = arg
        if opt in ('-l', '--level'):
            ecc_level = arg
        if opt in ('-p', '--path'):
            save_path = arg

    Qrcode(word, ecc_level).generate(save_path)
