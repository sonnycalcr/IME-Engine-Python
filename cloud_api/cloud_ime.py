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
                                res = json.loads(text)
                                return res
                            except json.JSONDecodeError:
                                print("Failed to decode JSON")
                                return text
                        else:
                            print(f"Error: {response.status}")
            except Exception as e:
                print(f"Request failed: {e}")
        return None


cloud_input_api = CloudinputApi()


async def fetch_cloud_results(quanpin_str: str):
    try:
        results = await cloud_input_api.get(quanpin_str)
        if results['errno'] != '0':  # pyright: ignore
            return " "
        return results["result"][0][0][0]  # pyright: ignore
    except asyncio.CancelledError:
        return []


async def fetch_cloud_results_task_test(quanpin_str: str):
    query_task = asyncio.create_task(fetch_cloud_results(quanpin_str))
    await asyncio.sleep(1)
    if query_task and query_task.done():
        res = query_task.result()
        print("what: ", str(res))


if __name__ == "__main__":
    # 测试
    cloud_input_api = CloudinputApi()
    print(asyncio.run(cloud_input_api.get("bai'jing'yuan")))
    print(asyncio.run(cloud_input_api.get("xi'hua'yuan")))
    print(asyncio.run(cloud_input_api.get("yun'yuan")))
    print(asyncio.run(cloud_input_api.get("dong'cao")))
    print(asyncio.run(cloud_input_api.get("dong'yuan")))
    print(asyncio.run(cloud_input_api.get("nimabinimasile")))
    print(asyncio.run(cloud_input_api.get("nimageshabidongxi")))
    print(asyncio.run(fetch_cloud_results("dong'yuan")))
    asyncio.run(fetch_cloud_results_task_test("dong'yuan"))
