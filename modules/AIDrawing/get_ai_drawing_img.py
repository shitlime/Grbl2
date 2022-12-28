import base64
import aiohttp
import asyncio
import requests

#TEST
from pathlib import Path
from urllib import request

# 服务器
server_list = [ "https://lulu.uedbq.xyz", "http://91.217.139.190:5010", "http://185.80.202.180:5010/", "http://185.80.202.180:5010/"]
server = server_list[1]

def get_img(url: str):
#    headers = {
#        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'''
#        }
    headers = {
        'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'''
        }
    req = request.Request(url, headers=headers)
    img = request.urlopen(req)
    return img.read()

def get_img_2(url: str):
    img = requests.get(url, timeout=(25, 35), headers={
            'Connection': 'close'})
    return img.content

async def get_img_3(url: str):
    headers={
    'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36''',
    'Connection': 'close'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            if r.status == 200:
                img = await r.read()
                print(f"img size{len(img)}")
                if len(img) < 5120:
                    return None
                return img
            else:
                return r.status

async def put_img(img: bytes, url: str):
    headers={
    'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36''',
    'Connection': 'close'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=url, data=img) as r:
            if r.status == 200:
                i = await r.read()
                print(f"img size{len(i)}")
                if len(i) < 5120:
                    return None
                return i
            else:
                return r.status

async def get_img_from_tags(token: str, tags: str):
    """
    用tags向服务器发送请求并返回base64的图片\n\n
    token: 服务器接受的认证token\n
    tags: 绘制图片的标签tag\n
    """
    url = f"{server}/got_image?&token={token}&tags={tags}&r18=0"
    try:
        img = await get_img_3(url)
        if type(img) == bytes:
            img = base64.b64encode(img)    # 非异步函数，不能加await
            return img    # 正常请求，返回图片
        else:
            print(f'AI画图网络请求{img}错误！')
            return img    # 错误请求，返回错误码
    except:
        print('AI画图出现错误！')
        return None    # 未知错误，返回None

async def get_img_from_img(token: str, i_img: bytes):
    """
    用图片向服务器请求并返回base64的图片\n\n
    token: 服务器接受的认证token\n
    i_img: input image输入的图片\n
    """
    url = f"{server}/got_image2image?&token={token}&strength=0.7"
    try:
        r_img = await put_img(i_img, url)
        if type(r_img) == bytes:
            r_img = base64.b64encode(r_img)
            return r_img
        else:
            print(f'AI以图生图网络请求{r_img}错误！')
            return r_img
    except:
        print('AI以图生图出现错误！')
        return None
    pass

#TEST
if __name__ == "__main__":
    token = input('token: ')
# AI tag画图
    tags="1girl"
    #i = get_ai_drawing_img(token, tags)
    loop = asyncio.get_event_loop()
    i = loop.run_until_complete(get_img_from_tags(token, tags))
    #print(i)
    print(type(i))
    #Path('C:\\Users\\17531\\Desktop\\1.jpg').write_bytes(i)

# AI以图生图
#    i_img = Path('C:\\Users\\17531\\Desktop\\1.jpg').read_bytes()
#    i_img = base64.b64encode(i_img)
#    loop = asyncio.get_event_loop()
#    i = loop.run_until_complete(get_img_from_img(token, i_img))
#    print(type(i))
#    Path('C:\\Users\\17531\\Desktop\\r_1.png').write_bytes(i)