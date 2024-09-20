"""
小鹤双拼 + 辅助码
"""

import os.path


class XiaoheShuangpin:
    def __init__(self) -> None:
        # 声母映射
        self.sm_keymaps = {"sh": "u", "ch": "i", "zh": "v"}
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
        pinyin_file_path = os.path.join(os.path.dirname(__file__), "./pinyin.txt")
        with open(pinyin_file_path, "r") as file:
            all_lines = file.readlines()
            for each_line in all_lines:
                cur_line = each_line.strip()
                if cur_line not in self.quanpin_tbl:
                    self.quanpin_tbl.add(cur_line)
                else:
                    print(cur_line)
        print(len(self.quanpin_tbl))


    def cvt_single_pinyin_to_sp(self, pinyin: str) -> str:
        """
        把单个拼音(全拼)转换为小鹤双拼
        """
        if len(pinyin) == 1:
            # 如果是 n、a 这种单声母或者韵母，且，是单字母的拼音，虽然 n 比较特殊，但是，这个因为 niao 本身所拥有的字数并不算多，所以可以并在一起
            pinyin = pinyin * 2
        elif len(pinyin) == 2:
            # 双字母保持全拼方式，如：li，xi，wu，ng，an
            pinyin = pinyin
        elif len(pinyin) > 2:
            # 如果是 ang 这种单韵母拼音，且为三字母，规则是首字母加韵母所在键
            if pinyin in self.sm_keymaps.keys():
                pinyin = pinyin[0] + self.sm_keymaps[pinyin]
            # 如果声母是两个字母
            elif pinyin[:2] in self.sm_keymaps.keys():
                pinyin = self.sm_keymaps[pinyin[:2]] + self.ym_keymaps[pinyin[2:]]
            # 声母是单字母
            else:
                pinyin = pinyin[0] + self.ym_keymaps[pinyin[1:]]
        return pinyin

    def cvt_single_sp_to_pinyin(self, sp_str: str) -> list[str]:
        """
        把小鹤双拼转换为拼音(全拼)
        """
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
            res.append(sm + each_ym)
        return res


if __name__ == "__main__":
    xiaohe_shuangpin = XiaoheShuangpin()
    print(xiaohe_shuangpin.cvt_single_sp_to_pinyin("ul"))
