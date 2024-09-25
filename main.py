import os
import sys
import readchar
import curses


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from cloud_api.cloud_ime import CloudinputApi
from xiaohe_sp.xiaohe_sp import XiaoheShuangpin
from quanpin.quanpin import Quanpin

stdscr = curses.initscr()
curses.curs_set(0) # 直接把光标给隐藏掉
stdscr.leaveok(False)  # 防止闪烁，但是似乎无法完全避免
stdscr.idcok(False)
stdscr.idlok(False)
cloud_api_tool = CloudinputApi()
xiaohe_sp_tool = XiaoheShuangpin()

if __name__ == "__main__":
    pinyin_str = ""
    han_str = ""  # 汉字
    with Quanpin() as quanpin_tool:
        while True:
            cur_char = readchar.readchar()
            if cur_char >= 'a' and cur_char <= 'z':
                pinyin_str += cur_char
            elif cur_char == readchar.key.BACKSPACE:
                if len(pinyin_str) > 0:
                    pinyin_str = pinyin_str[:-1]

            stdscr.erase()
            stdscr.addstr(0, 0, pinyin_str + "⎸") # 
            sp_str = xiaohe_sp_tool.pinyin_segmentation(pinyin_str)
            quanpin_str = xiaohe_sp_tool.quanpin_segmentation_from_sp(sp_str)
            stdscr.addstr(1, 0, "双拼：" + sp_str)
            stdscr.addstr(2, 0, "全拼：" + quanpin_str)

            if len(pinyin_str) > 0:
                query_results = quanpin_tool.query_words_limit_40(quanpin_str, sp_str)
                candidate_list = ["" for _ in range(8)]
                range_len = 8 if len(query_results) > 8 else len(query_results)
                for i in range(range_len):
                    candidate_list[i] = query_results[i]
                    stdscr.addstr(3 + i, 0, str(i + 1) + ". " + str(candidate_list[i][2]))

            stdscr.move(0, len(pinyin_str))
            stdscr.refresh()
            if (cur_char == readchar.key.CTRL_C):
                break
