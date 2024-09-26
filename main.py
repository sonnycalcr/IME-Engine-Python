import os
import sys
import readchar
import curses
import asyncio


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from cloud_api.cloud_ime import CloudinputApi
from xiaohe_sp.xiaohe_sp import XiaoheShuangpin
from quanpin.quanpin import Quanpin

stdscr = curses.initscr()
curses.curs_set(0)  # 直接把光标给隐藏掉
stdscr.leaveok(False)  # 防止闪烁，但是似乎无法完全避免
stdscr.idcok(False)
stdscr.idlok(False)
cloud_api_tool = CloudinputApi()
xiaohe_sp_tool = XiaoheShuangpin()

"""
TODO: 
让 cloud_api_tool 生成的条目动态插入到候选框(candidate_list)的第二个位置，并且，不能影响主流程，云输入生成的结果是可选项，如果在当前的拼音字符串的情况下，并且暂时没有其他键盘操作了，这时候，如果云输入接口返回响应体了，那么，动态插入到候选列表的第二位置(其他的选项往后挪)，而如果此时被其他输入打断，重新开始请求新的云输入数据。

疑问：能否可以用多进程/线程完成？不需要考虑优雅美观，能用就行，这个 py 项目只是一个演示和算法验证。
"""
async def main():
    pinyin_str = ""
    han_str = ""  # 汉字
    query_task = None
    stdscr.addstr(0, 0, "⎸")
    stdscr.refresh()
    with Quanpin() as quanpin_tool:
        while True:
            cur_char = readchar.readchar()
            if cur_char >= 'a' and cur_char <= 'z':
                pinyin_str += cur_char
            elif cur_char == readchar.key.BACKSPACE:
                if len(pinyin_str) > 0:
                    pinyin_str = pinyin_str[:-1]

            stdscr.erase()
            stdscr.addstr(0, 0, han_str + pinyin_str + "⎸")
            sp_str = xiaohe_sp_tool.pinyin_segmentation(pinyin_str)
            quanpin_str = xiaohe_sp_tool.quanpin_segmentation_from_sp(sp_str)
            stdscr.addstr(1, 0, "小鹤双拼：" + sp_str)
            stdscr.addstr(2, 0, "拼音全拼：" + quanpin_str)

            if len(pinyin_str) > 0:
                if query_task and not query_task.done():
                    query_task.cancel()
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

    curses.curs_set(2)  # 恢复光标(其实是 caret)可见性

if __name__ == "__main__":
    asyncio.run(main())
