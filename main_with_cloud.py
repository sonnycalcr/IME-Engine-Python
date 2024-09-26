import os
import sys
import curses
import asyncio
import readchar
from concurrent.futures import ThreadPoolExecutor


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


async def fetch_cloud_results(quanpin_str: str):
    try:
        results = await cloud_api_tool.get(quanpin_str)
        if results['errno'] != '0':  # pyright: ignore
            return " "
        return results["result"][0][0][0]  # pyright: ignore
    except asyncio.CancelledError:
        return []


async def read_input(loop, queue):
    with ThreadPoolExecutor() as pool:
        while True:
            char = await loop.run_in_executor(pool, readchar.readchar)  # 等待键盘输入
            # 将输入放入 queue1，供 second_task 使用
            await queue.put(char)
            # 按下 'Ctrl + C' 时退出
            if char == readchar.key.CTRL_C:
                break


async def ime_task(queue):
    cur_char = ""
    pinyin_str = ""  # 到目前为止的用户输入的拼音字符串
    han_str = ""  # 汉字
    sp_str = ""
    quanpin_str = ""
    range_len = 0
    query_task = None
    candidate_list = ["" for _ in range(8)]
    stdscr.addstr(0, 0, "⎸")
    stdscr.refresh()
    with Quanpin() as quanpin_tool:
        while True:
            # 获取来自 read_input 的数据
            try:
                cur_char = queue.get_nowait()
                # 处理键盘输入
                # 按下 'Ctrl + C' 时退出
                if cur_char == readchar.key.CTRL_C:
                    break
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
                    range_len = 8 if len(query_results) > 8 else len(query_results)
                    candidate_list = ["" for _ in range(8)]  # 先清空一下
                    for i in range(range_len):
                        candidate_list[i] = query_results[i]
                        stdscr.addstr(4 + i, 0, str(i + 2) + ". " + str(candidate_list[i][2]))

                    # 异步查询云输入结果
                    if query_task:
                        query_task.cancel()
                    query_task = asyncio.create_task(fetch_cloud_results(quanpin_str))
                stdscr.refresh()

            except asyncio.QueueEmpty:
                if len(pinyin_str) == 0:
                    stdscr.erase()
                    stdscr.addstr(0, 0, han_str + pinyin_str + "⎸")
                    sp_str = xiaohe_sp_tool.pinyin_segmentation(pinyin_str)
                    quanpin_str = xiaohe_sp_tool.quanpin_segmentation_from_sp(sp_str)
                    stdscr.addstr(1, 0, "小鹤双拼：" + sp_str)
                    stdscr.addstr(2, 0, "拼音全拼：" + quanpin_str)
                    # stdscr.addstr(3, 0, "1. " + '  ')
                    stdscr.refresh()
                elif query_task and query_task.done():
                    cloud_result = query_task.result()
                    stdscr.addstr(13, 0, str(cloud_result))
                    stdscr.erase()
                    stdscr.addstr(0, 0, han_str + pinyin_str + "⎸")
                    stdscr.addstr(1, 0, "小鹤双拼：" + sp_str)
                    stdscr.addstr(2, 0, "拼音全拼：" + quanpin_str)
                    stdscr.addstr(3, 0, "1. " + str(cloud_result) + " ")
                    for i in range(range_len):
                        stdscr.addstr(4 + i, 0, str(i + 2) + ". " + str(candidate_list[i][2]))
                    stdscr.refresh()
                await asyncio.sleep(0.012)  # 大致保证在 1000/60 ms 这个范围内就差不多了，60 是我的屏幕的刷新率
    curses.curs_set(2)  # 恢复光标(其实是 caret)可见性


async def main():
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()  # 用于 read_input -> ime_task 的数据传递
    # 同时运行 read_input 和 ime_task
    await asyncio.gather(
        read_input(loop, queue),
        ime_task(queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
