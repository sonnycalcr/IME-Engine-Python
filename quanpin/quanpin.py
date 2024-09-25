"""
全拼的 api

因为目前实际上只是为双拼服务的，所以，这里用来查询的全拼字符串并不覆盖所有可能的情况
"""

import sqlite3
from typing import Optional, Any
import sys
import os.path
import re


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from xiaohe_sp.xiaohe_sp import XiaoheShuangpin

default_db_path = os.path.join(os.path.dirname(__file__), "../assets/imeciku.db")

class Quanpin:
    def __init__(self, db_path: str = default_db_path) -> None:
        self.db_path: str = db_path
        self.conn: sqlite3.Connection
        self.singlechar_zero_sms = ["a", "e", "o"]  # 单个字符的零声母
        self.xiaohe_sp_helper = XiaoheShuangpin()
        self.max_len_of_single_pinyin = 6  # 比如：床

    def __enter__(self) -> 'Quanpin':
        self.conn = sqlite3.connect(self.db_path)

        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None
        self.conn.create_function("REGEXP", 2, regexp)  # sqlite 原生不支持正则
        return self

    def __exit__(self, exc_type: Optional[type], exc_value: Optional[Exception], traceback: Optional[Any]) -> None:
        if self.conn:
            self.conn.close()

    def _is_pure_jp_(self, pinyin_str: str, sp_str: str):
        """
        必须同时借助全拼和双拼这二者的拼音分词来确定是否是简拼
        """
        return all(len(single_pinyin) == 1 for single_pinyin in pinyin_str.split("'")) and all(len(single_sp) == 1 for single_sp in sp_str.split("'"))

    def _is_pure_quanpin_(self, pinyin_str: str, sp_str: str):
        """
        最好同时借助全拼和双拼这二者的拼音分词来确定是否是简拼
        """
        return all(len(single_pinyin) >= 1 for single_pinyin in pinyin_str.split("'")) and all(len(single_sp) == 2 for single_sp in sp_str.split("'"))

    def _extract_jp_(self, pinyin: str) -> str:
        """
        提取简拼
        """
        if "'" not in pinyin:
            return pinyin[0]
        else:
            return "'".join(s[0] for s in pinyin.split("'"))

    def query_words_limit_40(self, pinyin_str: str, sp_str: str) -> list[Any]:
        if self._is_pure_jp_(pinyin_str, sp_str):
            sql_str = """select key, jp, value, weight from quanpintbl where jp = ? order by weight desc limit 40"""
            cursor = self.conn.cursor()
            cursor.execute(sql_str, (sp_str,))
            results = cursor.fetchall()
            return results
        elif self._is_pure_quanpin_(pinyin_str, sp_str):
            sql_str = """select key, jp, value, weight from quanpintbl where key = ? order by weight desc limit 40"""
            cursor = self.conn.cursor()
            cursor.execute(sql_str, (pinyin_str,))
            results = cursor.fetchall()
            return results
        else:
            sql_str = """select key, jp, value, weight from quanpintbl where jp = ? and key REGEXP ? order by weight desc limit 40"""
            jp_sql_var = self._extract_jp_(pinyin_str)
            fuzzy_var = ""
            split_quanpin = pinyin_str.split("'")
            for single_pinyin in split_quanpin:
                if single_pinyin in self.xiaohe_sp_helper.quanpin_tbl:
                    fuzzy_var = fuzzy_var + "'" + single_pinyin
                else:  # 由双拼切割而来的，这里肯定是一个声母
                    fuzzy_var = fuzzy_var + "'" + single_pinyin + "[a-z][a-z]?[a-z]?[a-z]?"  # 单字符/双字符声母的最大韵母长度都是 4
            fuzzy_var = fuzzy_var.strip("'")
            cursor = self.conn.cursor()
            cursor.execute(sql_str, (jp_sql_var, fuzzy_var,))
            results = cursor.fetchall()
            return results


if __name__ == "__main__":
    with Quanpin() as quanpin:
        # pure jp test
        results = quanpin.query_words_limit_40("j'k", "j'k")
        print(results)
        results = quanpin.query_words_limit_40("j'j", "j'j")
        print(results)
        results = quanpin.query_words_limit_40("j'j'k", "j'j'k")
        print(results)
        # pure quanpin test
        results = quanpin.query_words_limit_40("ni'hao", "ni'hc")
        print(results)
        results = quanpin.query_words_limit_40("bai'jing'yuan", "bd'jk'yr")
        print(results)
        # 更一般的情况
        results = quanpin.query_words_limit_40("j'ji'ka", "j'ji'ka")
        print(results)
        results = quanpin.query_words_limit_40("j'jia'jia", "j'jx'jx")
        print(results)
