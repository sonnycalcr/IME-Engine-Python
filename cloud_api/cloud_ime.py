import requests

class CloudinputApi:
    def __init__(self):
        self.req = None
        self.py = ""
        self.flag = 0
        self.api = "http://olime.baidu.com/py?input={}&inputtype=py&bg=0&ed=20&result=hanzi&resultcoding=utf-8&ch_en=0&clientinfo=web&version=1"

    def get(self, input_str):
        if self.flag:
            self.flag = 0
            # In Python, we can't abort a request easily, so we don't need this

        if input_str:
            try:
                url = self.api.format(input_str)
                self.flag = 1
                response = requests.get(url, timeout=10)  # 设定超时
                if response.status_code == 200:
                    self.flag = 0
                    return response.json()  # 或者 `response.text` 根据 API 返回的格式
                else:
                    print(f"Error: {response.status_code}")
            except Exception as e:
                print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    # 示例使用:
    cloud_input_api = CloudinputApi()
    result = cloud_input_api.get('jiangshanruhua')
    if result:
        print(result)

    result = cloud_input_api.get('nishuoshenme')
    if result:
        print(result)

    result = cloud_input_api.get('nitiandongxi')
    if result:
        print(result)

    result = cloud_input_api.get('yuantengfei')
    if result:
        print(result)

    result = cloud_input_api.get('baijingyuan')
    if result:
        print(result)

    result = cloud_input_api.get('baijingyuan')
    if result:
        print(result)

    result = cloud_input_api.get('niema')
    if result:
        print(result)

    result = cloud_input_api.get('shabi')
    if result:
        print(result)

    result = cloud_input_api.get('hhhhhhhhh')
    if result:
        print(result)

    result = cloud_input_api.get("bai'jing'yuan")
    if result:
        print(result)

    result = cloud_input_api.get("tian")
    if result:
        print(result)

    result = cloud_input_api.get("xian")
    if result:
        print(result)

    result = cloud_input_api.get("xi'an")
    if result:
        print(result)

    result = cloud_input_api.get("ni'zhen'shi'ge'ni'tian'dong'xi")
    if result:
        print(result)

    """
    经过测试，发现脏话的输出为空，并返回相应的错误码。
    """

    """
    output:
    {'errmsg': '', 'errno': '0', 'result': [[['江山如画', 14, {'pinyin': "jiang'shan'ru'hua", 'type': 'IMEDICT'}]], "jiang'shan'ru'hua"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['你说什么', 12, {'pinyin': "ni'shuo'shen'me", 'type': 'IMEDICT'}]], "ni'shuo'shen'me"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['逆天东西', 12, {'pinyin': "ni'tian'dong'xi", 'type': 'IMEDICT'}]], "ni'tian'dong'xi"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['袁腾飞', 11, {'pinyin': "yuan'teng'fei", 'type': 'IMEDICT'}]], "yuan'teng'fei"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['百景园', 11, {'pinyin': "bai'jing'yuan", 'type': 'IMEDICT'}], ['白景元', 11, {'pinyin': "bai'jing'yuan", 'type': 'IMEDICT'}]], "bai'jing'yuan"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['百景园', 11, {'pinyin': "bai'jing'yuan", 'type': 'IMEDICT'}], ['白景元', 11, {'pinyin': "bai'jing'yuan", 'type': 'IMEDICT'}]], "bai'jing'yuan"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['捏马', 5, {'pinyin': "nie'ma", 'type': 'IMEDICT'}], ['捏吗', 5, {'pinyin': "nie'ma", 'type': 'IMEDICT'}]], "nie'ma"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['沙币', 5, {'pinyin': "sha'bi", 'type': 'IMEDICT'}]], "sha'bi"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['哈哈哈哈哈哈哈哈哈', 18, {'pinyin': "ha'ha'ha'ha'ha'ha'ha'ha'ha", 'type': 'IMEDICT'}]], "ha'ha'ha'ha'ha'ha'ha'ha'ha"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['百景园', 11, {'pinyin': "bai'jing'yuan", 'type': 'IMEDICT'}]], "bai'jing'yuan"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['天', 4, {'pinyin': 'tian', 'type': 'IMEDICT'}], ['填', 4, {'pinyin': 'tian', 'type': 'IMEDICT'}], ['田', 4, {'pinyin': 'tian', 'type': 'IMEDICT'}], ['甜', 4, {'pinyin': 'tian', 'type': 'IMEDICT'}]], 'tian'], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['先', 4, {'pinyin': 'xian', 'type': 'IMEDICT'}], ['线', 4, {'pinyin': 'xian', 'type': 'IMEDICT'}], ['现', 4, {'pinyin': 'xian', 'type': 'IMEDICT'}]], 'xian'], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['西安', 4, {'pinyin': "xi'an", 'type': 'IMEDICT'}]], "xi'an"], 'status': 'T'}
    {'errmsg': '', 'errno': '0', 'result': [[['你真是个你填东西', 23, {'pinyin': "ni'zhen'shi'ge'ni'tian'dong'xi", 'type': 'IMEDICT'}]], "ni'zhen'shi'ge'ni'tian'dong'xi"], 'status': 'T'}
    """
