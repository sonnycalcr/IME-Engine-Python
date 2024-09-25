import aiohttp
import asyncio
import json


class CloudinputApi:
    def __init__(self):
        self.req = None
        self.py = ""
        self.flag = 0
        self.api = "http://olime.baidu.com/py?input={}&inputtype=py&bg=0&ed=20&result=hanzi&resultcoding=utf-8&ch_en=0&clientinfo=web&version=1"

    async def get(self, input_str):
        if self.flag:
            self.flag = 0

        if input_str:
            try:
                url = self.api.format(input_str)
                self.flag = 1
                timeout = aiohttp.ClientTimeout(total=10)  # 设置超时
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=timeout) as response:
                        if response.status == 200:
                            self.flag = 0
                            text = await response.text()
                            try:
                                return json.loads(text)
                            except json.JSONDecodeError:
                                print("Failed to decode JSON")
                                return text
                        else:
                            print(f"Error: {response.status}")
            except Exception as e:
                print(f"Request failed: {e}")
        return None


if __name__ == "__main__":
    # 测试
    cloud_input_api = CloudinputApi()
    print(asyncio.run(cloud_input_api.get("bai'jing'yuan")))
    print(asyncio.run(cloud_input_api.get("xi'hua'yuan")))
    print(asyncio.run(cloud_input_api.get("yun'yuan")))
    print(asyncio.run(cloud_input_api.get("dong'cao")))
    print(asyncio.run(cloud_input_api.get("dong'yuan")))
