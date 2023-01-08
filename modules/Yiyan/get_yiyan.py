import aiohttp
import asyncio

# 获取一言

async def get_yiyan(c: list[str], encode: str, min_length=1, max_length=100):
    """
    通过参数访问, 返回一个一言API结果
    c: 句子类型 (a:动画|b:漫画|c:游戏|d:文学|e:原创|f:来自网络|g:其他|h:影视|i:诗词|j:网易云|k:哲学|l:抖机灵)
    encode: 返回格式 (text: 纯文本|json:格式化的JSON)
    min_length: 返回句子的最小长度（包含）
    max_length: 返回句子的最大长度（包含）

    Returns: API结果
    """
    c = '&c='.join(c)    # 合并c参数
    url_yiyan = f"https://v1.hitokoto.cn/?c={c}&encode={encode}&charset=utf-8&min_length={min_length}&max_length={max_length}"
    # DEBUG
    #print(f"url_yiyan={url_yiyan}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url_yiyan) as r:
            if r.status == 200:
                if encode == 'text':
                    text = await r.read()
                    return text.decode('utf-8')
                elif encode == 'json':
                    return await r.json()
                else:
                    print('指定的返回格式不合法')
                    return None
            else:
                return r.status

if __name__ == '__main__':
    c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    c2 = ['k', 'f']
    encode = 'json'
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_yiyan(c=c, encode=encode))
    print('--------------')
    print(f"result = {result}")
    print(f"type result:{type(result)}")

    # json mode only
    print('--------------')
    m1 = result['hitokoto']
    m2 = result['from_who']
    m3 = result['from']
    if m2 == None:
        m2 = ''
    if m3 == None:
        m3 = ''
    print(f"{m1}\n\t——{m2} {m3}")