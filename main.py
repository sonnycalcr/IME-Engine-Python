import os
import sys
import readchar
import curses


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from cloud_api.cloud_ime import CloudinputApi
from xiaohe_sp.xiaohe_sp import XiaoheShuangpin
from quanpin.quanpin import Quanpin

stdscr = curses.initscr()
stdscr.leaveok(False)
cloud_api_tool = CloudinputApi()
xiaohe_sp_tool = XiaoheShuangpin()

if __name__ == "__main__":
    pinyin_str = ""
    with Quanpin() as quanpin_tool:
        while True:
            cur_char = readchar.readchar()
            if cur_char >= 'a' and cur_char <= 'z':
                pinyin_str += cur_char
            elif cur_char == readchar.key.BACKSPACE:
                if len(pinyin_str) > 0:
                    pinyin_str = pinyin_str[:-1]
            stdscr.clrtobot()  # 清除光标之后的所有内容
            stdscr.refresh()
            stdscr.addstr(0, 0, pinyin_str)
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
            
            stdscr.move(0, len(pinyin_str))  # 清除光标所在行的光标后面所有的内容
            stdscr.clrtoeol()
            stdscr.refresh()
            if (cur_char == readchar.key.CTRL_C):
                break
