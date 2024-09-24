import os
import sys
import readchar
import curses


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from cloud_api.cloud_ime import CloudinputApi
from xiaohe_sp.xiaohe_sp import XiaoheShuangpin

stdscr = curses.initscr()

if __name__ == "__main__":
    pinyin_str = ""
    while True:
        cur_char = readchar.readchar()
        if cur_char >= 'a' and cur_char <= 'z':
            pinyin_str += cur_char
        elif cur_char == readchar.key.BACKSPACE:
            if len(pinyin_str) > 0:
                pinyin_str = pinyin_str[:-1]
        # print(pinyin_str, end='\r')
        sys.stdout.write("%s\r" % "                                                                              ")
        sys.stdout.write("%s\r" % pinyin_str)
        sys.stdout.flush()
        if (cur_char == readchar.key.CTRL_C):
            break
