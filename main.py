import os
import sys
import readchar


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from cloud_api.cloud_ime import CloudinputApi
from xiaohe_sp.xiaohe_sp import XiaoheShuangpin


if __name__ == "__main__":
    pinyin_str = ""
    while True:
        cur_char = readchar.readchar()
        pinyin_str += cur_char
        print(pinyin_str)
        if (cur_char == readchar.key.CTRL_C):
            break

        
