import re
import asyncio
import aiohttp
from bilibili_api import video


def get_video_id(url: str) -> str | None:
    """提取url中的视屏id"""
    id = re.search(r"BV[A-Za-z0-9]+|av[0-9]+|bv[A-Za-z0-9]+", url)
    if id:
        return id.group()

def get_video(id: str):
    """根据视频id获取Video对象"""
    if id.startswith(("BV", "bv")):
        v = video.Video(bvid=id)
    if id.startswith("av"):
        id = int(id[2:])  # aid必须是int
        v = video.Video(aid=id)
    return v

async def get_url(string: str):
    """从字符串中提取视频相关URL"""
    url = re.search(".*?(https?://b23.tv/[A-Za-z0-9]+).*?", string)
    if url:
        return await get_real_url(url.group(1))
    else:
        return string

async def get_real_url(url: str):
    """从手机端分享的链接转换成普通链接"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            if result.status == 200:
                print(result.url)
                return str(result.url)

async def get_video_info(string: str) -> dict | None:
    # 输入信息
    url = await get_url(string)
    id = get_video_id(url)
    # 实例化 Video 类
    if id != None:
        v = get_video(id)
        # 获取信息
        try:
            info = await v.get_info()
            # 打印信息
            print(str(info)[:3000])
            return info
        except:
            print("获取视频信息出错了")

if __name__ == '__main__':
    string = input("输入视屏链接：")
    asyncio.get_event_loop().run_until_complete(get_video_info(string))