import re
import asyncio
import aiohttp

trime_nightly_release = "https://github.com/osfans/trime/releases/tag/nightly"

async def get_nightly_commit_hash():
    """
    访问github获取信息，组装成下载链接返回
    """
    commit_hash_pattern = r'data-hovercard-type="commit".+?href="/osfans/trime/commit/(.{8})'
    async with aiohttp.ClientSession() as session:
        async with session.get(trime_nightly_release) as r:
            if r.status == 200:
                html = await r.read()
                html = html.decode('utf-8')
                commit_hash = re.search(commit_hash_pattern, html).group(1)
                return commit_hash
            else:
                return r.start

def generate_nightly_download_link(commit_hash: str) -> list:
    url_preix = "https://github.com/osfans/trime/releases/download/nightly/"
    return [f"{url_preix}com.osfans.trime-nightly-0-g{commit_hash}-arm64-v8a-release.apk",
            f"{url_preix}com.osfans.trime-nightly-0-g{commit_hash}-armeabi-v7a-release.apk",
            f"{url_preix}com.osfans.trime-nightly-0-g{commit_hash}-x86-release.apk",
            f"{url_preix}com.osfans.trime-nightly-0-g{commit_hash}-x86_64-release.apk"]

async def get_all_file_info() -> dict:
    commit_hash = await get_nightly_commit_hash()
    if type(commit_hash) == str:
        link = generate_nightly_download_link(commit_hash)
        # 生成字典格式： {文件名: 下载链接}
        d = {}
        for l in link:
            d[l.split("/")[-1]] = l
        print(d)
        return d
    else:
        print(f"获取trime nightly commit hash出错！状态码：{commit_hash}")

async def get_file_bytes(url: str):
    """
    通过链接下载文件数据，返回bytes
    """
    async with aiohttp.request("GET", url=url) as r:
        return await r.read()

async def test():
    commit_hash = await get_nightly_commit_hash()
    if type(commit_hash) == str:
        link = generate_nightly_download_link(commit_hash)
        print('\n'.join(link))
        data = await get_file_bytes(link[0])
        print(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())