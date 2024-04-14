import re
import asyncio
import aiohttp
from bilibili_api import video
from loguru import logger


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
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Connection': 'close'
    }
    timeout = aiohttp.ClientTimeout(total = 30)
    logger.info(f"Bilibili.get_real_url: 开始访问手机端分享链接 {url}")
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        async with session.get(url) as result:
            if result.status == 200:
                logger.info(f"Bilibili.get_real_url: 获取到原始链接 {result.url}")
                return str(result.url)
            else:
                logger.error(f"Bilibili.get_real_url: 返回结果错误，状态码 {result.status}")

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
            logger.info(f"视频信息：{str(info)[:500]}")
            return info
        except:
            logger.error("获取视频信息失败了")

async def get_video_ai_conclusion(string: str) -> dict:
    # 输入信息
    url = await get_url(string)
    id = get_video_id(url)
    # 实例化 Video 类
    if id != None:
        v = get_video(id)
        # 获取信息
        try:
            cid = list(await v.get_pages())[0]['cid']
            ai_conclusion = await v.get_ai_conclusion(cid)
            # 打印信息
            logger.info(f"AI总结：{str(ai_conclusion)[:500]}")
            return ai_conclusion
        except:
            logger.error("获取视频AI总结失败了")

if __name__ == '__main__':
    string = input("输入视屏链接：")
    # asyncio.get_event_loop().run_until_complete(get_video_info(string))
    asyncio.get_event_loop().run_until_complete(get_video_ai_conclusion(string))