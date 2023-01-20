import aiohttp
import base64
import asyncio
import json

async def get_news_img() -> bytes | int:
    """
    获取60秒看世界的新闻图片
    Returns: bytes | int
    """
    api_url = 'http://bjb.yunwj.top/php/tp/lj.php'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as result:
            if result.status == 200:
                data = await result.read()
                data_json = json.loads(data)
                img_url = data_json['tp1']
                async with session.get(img_url) as r:
                    if r.status == 200:
                        img = await r.read()
                        return base64.b64encode(img)
                    else:
                        return result.status
            else:
                return result.status

# TEST
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    b64img = loop.run_until_complete(get_news_img())
    print(b64img)
    print(type(b64img))