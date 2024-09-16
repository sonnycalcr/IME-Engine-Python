"""
小鹤双拼 + 辅助码
"""


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
        self.quanpin_table = {
            "i": {"1": "i"},
            "u": {"1": "u"},
            "v": {"1": "v"},
            "a": {"1": "a", "ai": "i", "an": "n", "ang": "ng", "ao": "o"},
            "b": {"1": "b", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ian": "ian", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "o": "o", "u": "u", "un": "un"},
            "c": {"1": "c", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo"},
            "ch": {"1": "ch", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "ua": "ua", "uai": "uai", "uan": "uan", "uang": "uang", "ui": "ui", "un": "un", "uo": "uo"},
            "d": {"1": "d", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "en": "en", "ei": "ei", "eng": "eng", "i": "i", "ia": "ia", "ian": "ian", "iao": "iao", "ie": "ie", "ing": "ing", "iu": "iu", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo"},
            "e": {"1": "e", "ei": "i", "en": "n", "eng": "ng", "er": "r"},
            "f": {"1": "f", "a": "a", "an": "an", "ang": "ang", "ei": "ei", "en": "en", "eng": "eng", "iao": "iao", "o": "o", "ou": "ou", "u": "u"},
            "g": {"1": "g", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "ua": "ua", "uai": "uai", "uan": "uan", "uang": "uang", "ui": "ui", "un": "un", "uo": "uo"},
            "h": {"1": "h", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "ua": "ua", "uai": "uai", "uan": "uan", "uang": "uang", "ui": "ui", "un": "un", "uo": "uo"},
            "j": {"1": "j", "i": "i", "ia": "ia", "ian": "ian", "iang": "iang", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "iong": "iong", "iu": "iu", "u": "u", "uan": "uan", "ue": "ue", "un": "un", "v": "u", "van": "uan", "ve": "ue", "vn": "un"},
            "k": {"1": "k", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "en": "en", "eng": "eng", "ei": "ei", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "ua": "ua", "uai": "uai", "uan": "uan", "uang": "uang", "ui": "ui", "un": "un", "uo": "uo"},
            "l": {"1": "l", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "eng": "eng", "i": "i", "ia": "ia", "ian": "ian", "iang": "iang", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "iu": "iu", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "v": "v", "uan": "uan", "ue": "ue", "un": "un", "uo": "uo", "ve": "ue"},
            "m": {"1": "m", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ian": "ian", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "iu": "iu", "o": "o", "ou": "ou", "u": "u"},
            "n": {"1": "n", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ian": "ian", "iang": "iang", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "iu": "iu", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "v": "v", "uan": "uan", "ue": "ue", "uo": "uo", "un": "un", "ve": "ue"},
            "o": {"1": "o", "ou": "u"},
            "p": {"1": "p", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ian": "ian", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "o": "o", "ou": "ou", "u": "u"},
            "q": {"1": "q", "i": "i", "ia": "ia", "ian": "ian", "iang": "iang", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "iong": "iong", "iu": "iu", "u": "u", "uan": "uan", "ue": "ue", "un": "un", "van": "uan", "ve": "ue", "vn": "un", "v": "u"},
            "r": {"1": "r", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo"},
            "s": {"1": "s", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo"},
            "sh": {"1": "sh", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ou": "ou", "u": "u", "ua": "ua", "uai": "uai", "uan": "uan", "uang": "uang", "ui": "ui", "un": "un", "uo": "uo"},
            "t": {"1": "t", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "eng": "eng", "ei": "ei", "i": "i", "ian": "ian", "iao": "iao", "ie": "ie", "ing": "ing", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo"},
            "w": {"1": "w", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ei": "ei", "en": "en", "eng": "eng", "o": "o", "u": "u"},
            "x": {"1": "x", "i": "i", "ia": "ia", "ian": "ian", "iang": "iang", "iao": "iao", "ie": "ie", "in": "in", "ing": "ing", "iong": "iong", "iu": "iu", "u": "u", "uan": "uan", "un": "un", "ue": "ue", "van": "uan", "ve": "ue", "vn": "un", "v": "u"},
            "y": {"1": "y", "a": "a", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "i": "i", "in": "in", "ing": "ing", "o": "o", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ue": "ue", "un": "un", "v": "u", "van": "uan", "ve": "ue", "vn": "un"},
            "z": {"1": "z", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo"},
            "zh": {"1": "zh", "a": "a", "ai": "ai", "an": "an", "ang": "ang", "ao": "ao", "e": "e", "ei": "ei", "en": "en", "eng": "eng", "i": "i", "ong": "ong", "on": "ong", "ou": "ou", "u": "u", "uan": "uan", "ui": "ui", "un": "un", "uo": "uo", "ua": "ua", "uai": "uai", "uang": "uang"}
        }

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
