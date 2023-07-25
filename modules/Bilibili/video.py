import asyncio
import re
from bilibili_api import video

def get_video_id(url: str) -> str | None:
    """提取url中的视屏id"""
    id = re.search("BV[A-Za-z0-9]+|av[0-9]+|bv[A-Za-z0-9]+", url)
    if id != None:
        return id.group()

def get_video(id: str):
    """根据视频id获取Video对象"""
    if id.startswith(("BV", "bv")):
        v = video.Video(bvid=id)
    if id.startswith("av"):
        id = int(id[2:])  # aid必须是int
        v = video.Video(aid=id)
    return v

async def get_video_info(url: str) -> dict | None:
    # 输入信息
    id = get_video_id(url)
    # 实例化 Video 类
    if id != None:
        v = get_video(id)
        # 获取信息
        try:
            info = await v.get_info()
            # 打印信息
            print(info)
            return info
        except:
            print("获取视频信息出错了")

if __name__ == '__main__':
    url = input("输入视屏链接：")
    asyncio.get_event_loop().run_until_complete(get_video_info(url))