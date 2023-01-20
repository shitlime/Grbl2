import asyncio

from bot_init import BOT
from .get_60s_news import get_news_img

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema

channel = Channel.current()
channel.name("定时发送60秒看世界新闻")
channel.author("Shitlime")
channel.description("""
定时发送60秒看世界新闻

功能：每天在设定的时间发送60秒看世界的新闻
""")

config = BOT.get_modules_config("SixtySecNews")

# 配置：
enable_group = config["enable_group"]    # list
enable_friend = config["enable_friend"]    # list
send_time = config["send_time"]    # 遵循crontab的方式 例：'30 15 * * *'表示每天的15:30

# 定时发送：
@channel.use(SchedulerSchema(timer = timers.crontabify(send_time)))
async def send_news_img(app: Ariadne):
    i = 0
    news_img = await get_news_img()
    # 遇到错误将隔30s重试
    while type(news_img) != bytes and i < 16:
        print(f"请求新闻图片失败，错误码{news_img}，重试{i}…")
        news_img = await get_news_img()
        i += 1
        await asyncio.sleep(30)
    try:
        for group_num in enable_group:
            await app.send_group_message(
                target=group_num,
                message= MessageChain(
                    Image(base64=news_img),
                    Plain("请收好，这是今日份的报纸哦")
                )
            )
        for friend_num in enable_friend:
            await app.send_friend_message(
                target=friend_num,
                message= MessageChain(
                    Image(base64=news_img),
                    Plain("请收好，这是今日份的报纸哦")
                )
            )
    except:
        print("定时发送60秒看世界新闻 发送消息时错误")