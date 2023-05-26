import base64
import aiohttp
import asyncio

# TEST
from pathlib import Path

# 服务器
server_list = ['https://api.vvhan.com', 'https://183.146.28.96', 'https://123.6.81.234']
server = server_list[0]

async def get_img(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:    # 请求成功
                img = await r.read()
                print(f'acgimg size{len(img)}')
                return img
            else:    # 请求失败
                return r.status

async def get_acg_img():
    """
    无参数，调用直接返回一张acg图
    """
    url = f"{server}/api/acgimg"
    img = await get_img(url)
    if type(img) == bytes:
        return base64.b64encode(img)
    else:
        return img

# TEST
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    img = loop.run_until_complete(get_acg_img())
    if type(img) == bytes:
        img = base64.b64decode(img)
        Path('debug_temp.jpg').write_bytes(img)
    else:
        print(f'网络出错了: {img}')