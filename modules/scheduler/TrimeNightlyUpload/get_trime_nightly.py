import asyncio
import aiohttp
import datetime
import pytz

from OutdatedAssetsException import OutdatedAssetsException

github_api_trime_release = "https://api.github.com/repos/osfans/trime/releases?prerelease=true"

async def get_nightly_download_link():
    """
    访问github api获取信息，组装成下载链接返回
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(github_api_trime_release) as r:
            if r.status == 200:
                json = await r.json()
                # 找到nightly
                nightly = None
                for r in json:
                    if r['tag_name'] == "nightly":
                        nightly = r
                        break
                # 检查发布时间
                published_time = nightly['published_at']
                utc_time = datetime.datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%SZ")
                time = pytz.timezone("Asia/Shanghai").fromutc(utc_time)
                if time.date() != datetime.datetime.now().date() + datetime.timedelta(days=1):
                    raise OutdatedAssetsException("不是今天的nightly build")
                # 所有 release 文件信息
                assets = nightly['assets']
                return [ a['browser_download_url'] for a in assets ]
            else:
                return r.start

async def get_all_file_info() -> dict:
    links = await get_nightly_download_link()
    if type(links) == list:
        # 生成字典格式： {文件名: 下载链接}
        d = {}
        for l in links:
            d[l.split("/")[-1]] = l
        print(d)
        return d
    else:
        print(f"获取trime nightly下载链接出错！状态码：{links}")

async def get_file_bytes(url: str):
    """
    通过链接下载文件数据，返回bytes
    """
    async with aiohttp.request("GET", url=url) as r:
        return await r.read()

async def test():
    info = await get_all_file_info()
    data = await get_file_bytes(list(info.items())[0][1])
    print(data)
    print(len(data))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())