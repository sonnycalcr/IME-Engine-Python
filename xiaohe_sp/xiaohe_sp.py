"""
小鹤双拼 + 辅助码

零声母举例：
eng：鞥
ng 在大陆的词典里面读的是 ng，这个应该怎么映射到双拼呢？

教育部的pdf：http://www.moe.gov.cn/ewebeditor/uploadfile/2015/03/02/20150302165814246.pdf

关于 u 和 ü 的一点说明：

nue 这个全拼不应该存在，应该是 nve，也就是 nüe
同理，还有 lue 和 lve 之间的问题

j q x 要挖掉鱼的两点

TODO:
还有，我们小时候读的 en 的嗯字，现在被改成了鼻音的 ng，这个太特别了，以后可以单独加
"""

import os.path


class XiaoheShuangpin:
    def __init__(self) -> None:
        # 声母映射
        self.sm_keymaps = {"sh": "u", "ch": "i", "zh": "v"}
        self.sm_keymaps_reserved = {v: k for k, v in self.sm_keymaps.items()}
        # 零声母映射
        self.zero_sm_keymaps = {"a": "aa", "ai": "ai", "ao": "ao", "ang": "ah", "e": "ee",
                                "ei": "ei", "en": "en", "eng": "eg", "er": "er", "o": "oo", "ou": "ou"}
        self.zero_sm_keymaps_reversed = {v: k for k, v in self.zero_sm_keymaps.items()}
        # 韵母映射
        self.ym_keymaps = {
            "iu": "q",
            "ei": "w",
            "e": "e",
            "uan": "r",
            "ue": "t",
            "ve": "t",  # üe
            "un": "y",
            "u": "u",
            "i": "i",
            "uo": "o",
            "o": "o",
            "ie": "p",
            "a": "a",
            "ong": "s",
            "iong": "s",
            "ai": "d",
            "en": "f",
            "eng": "g",
            "ang": "h",
            "an": "j",
            "uai": "k",
            "ing": "k",
            "uang": "l",
            "iang": "l",
            "ou": "z",
            "ua": "x",
            "ia": "x",
            "ao": "c",
            "ui": "v",
            "v": "v",  # ü
            "in": "b",
            "iao": "n",
            "ian": "m",
        }
        self.quanpin_tbl = set()
        self.init_quanpin_tbl()

    def init_quanpin_tbl(self):
        pinyin_file_path = os.path.join(os.path.dirname(__file__), "../assets/pinyin.txt")
        with open(pinyin_file_path, "r") as file:
            all_lines = file.readlines()
            for each_line in all_lines:
                cur_line = each_line.strip()
                if cur_line not in self.quanpin_tbl:
                    self.quanpin_tbl.add(cur_line)

    def cvt_single_pinyin_to_sp(self, pinyin: str) -> str:
        """
        把单个拼音(全拼)转换为小鹤双拼

        注意：目前是一对一
        """
        if pinyin in self.zero_sm_keymaps.keys():
            return self.zero_sm_keymaps[pinyin]
        elif len(pinyin) == 2:
            # 双字母保持全拼方式，如：li，xi，wu，ng，an
            pinyin = pinyin
        elif len(pinyin) > 2:
            # 如果声母是两个字母
            if pinyin[:2] in self.sm_keymaps.keys():
                pinyin = self.sm_keymaps[pinyin[:2]] + self.ym_keymaps[pinyin[2:]]
            # 声母是单字母
            else:
                pinyin = pinyin[0] + self.ym_keymaps[pinyin[1:]]
        return pinyin

    def cvt_single_sp_to_pinyin(self, sp_str: str) -> list[str]:
        """
        把小鹤双拼转换为拼音(全拼)
        目前针对 402 个拼音是一对一的方案
        """
        if sp_str in self.zero_sm_keymaps.values():
            return [self.zero_sm_keymaps_reversed[sp_str]]
        if (len(sp_str) != 2):
            return []
        sm: str = ""
        ym_list: list[str] = []
        res = []
        if sp_str[0] in self.sm_keymaps.values():
            for key, value in self.sm_keymaps.items():
                if value == sp_str[0]:
                    sm = key
        else:
            sm = sp_str[0]
        for key, value in self.ym_keymaps.items():
            if sp_str[1] == value:
                ym_list.append(key)
        for each_ym in ym_list:
            if (sm + each_ym) in self.quanpin_tbl:
                res.append(sm + each_ym)
        if len(res) == 0: # 无法转换成全拼
            res.append("error")
        return res

    def pinyin_segmentation(self, sp_str: str) -> str:
        """
        切割双拼字符串，使用单引号 ' 作为切割符号
        使用正向最大划分来进行切割，也可以说是贪心法
        """
        if len(sp_str) == 1:
            return sp_str
        res = ''
        range_start = 0
        while range_start < len(sp_str):
            if (range_start + 2) <= len(sp_str):
                # 先切割两个字符看看
                cur_sp = sp_str[range_start:range_start + 2]
                if self.cvt_single_sp_to_pinyin(cur_sp)[0] in self.quanpin_tbl:
                    res = res + "'" + cur_sp
                    range_start += 2
                else:
                    res = res + "'" + cur_sp[0]
                    range_start += 1
            else:
                res = res + "'" + sp_str[-1]
                range_start += 1

        return res.strip("'")

    def quanpin_segmentation_from_sp(self, sp_seg_str: str) -> str:
        """
        将切割好的双拼字符串转换为全拼
        """
        split_sp_seg = sp_seg_str.split("'")
        res = ""
        for single_sp in split_sp_seg:
            if len(single_sp) == 2:
                res = res + "'" + self.cvt_single_sp_to_pinyin(single_sp)[0]
            else:
                if single_sp in self.sm_keymaps_reserved:
                    res = res + "'" + self.sm_keymaps_reserved[single_sp]
                else:
                    res = res + "'" + single_sp
        res = res.strip("'")
        return res


if __name__ == "__main__":
    # test
    xiaohe_shuangpin = XiaoheShuangpin()
    # 双拼转全拼测试
    print(xiaohe_shuangpin.cvt_single_sp_to_pinyin("ul"))
    print(xiaohe_shuangpin.cvt_single_sp_to_pinyin("qt"))
    print(xiaohe_shuangpin.cvt_single_sp_to_pinyin("xt"))
    print(xiaohe_shuangpin.cvt_single_sp_to_pinyin("lt"))
    # 双拼切割分词测试
    print(xiaohe_shuangpin.pinyin_segmentation("ulpb"))
    print(xiaohe_shuangpin.pinyin_segmentation("ulpbuiufmene"))
    print(xiaohe_shuangpin.pinyin_segmentation("nh"))
    print(xiaohe_shuangpin.pinyin_segmentation("nih"))
    print(xiaohe_shuangpin.pinyin_segmentation("v"))
    print(xiaohe_shuangpin.pinyin_segmentation("i"))
    print(xiaohe_shuangpin.pinyin_segmentation("u"))
    # 双拼分词转全拼分词测试
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("ulpb")))
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("ulpbuiufmene")))
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("nh")))
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("nih")))
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("v")))
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("i")))
    print(xiaohe_shuangpin.quanpin_segmentation_from_sp(xiaohe_shuangpin.pinyin_segmentation("u")))
