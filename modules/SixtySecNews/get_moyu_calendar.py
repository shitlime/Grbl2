import aiohttp
import base64
import asyncio

async def get_calendar_img() -> bytes | int:
    """
    获取摸鱼日历图片
    Returns: bytes | int
    """
    api_url = 'https://api.vvhan.com/api/moyu'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as result:
            if result.status == 200:
                data = await result.read()
                return base64.b64encode(data)
            else:
                return result.status

# TEST
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    b64img = loop.run_until_complete(get_calendar_img())
    print(b64img)
    print(len(b64img))
    print(type(b64img))