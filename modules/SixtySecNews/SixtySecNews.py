import asyncio

from bot_init import BOT
from modules.base.message_queue import MessageQueue
from .get_60s_news import get_news_img
from .get_moyu_calendar import get_calendar_img
from ..base.check import check_member, check_friend

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from graia.ariadne.model import Friend, Group
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.parser.twilight import(
    Twilight,
    UnionMatch,
)

channel = Channel.current()
channel.meta["name"]="定时发送60秒看世界新闻"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
定时发送60秒看世界新闻

功能：每天在设定的时间发送60秒看世界的新闻
"""

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
    calendar_img = await get_calendar_img()
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
                    Image(base64=calendar_img),
                    Image(base64=news_img),
                    Plain("请收好，这是今日份的报纸哦")
                )
            )
        for friend_num in enable_friend:
            await app.send_friend_message(
                target=friend_num,
                message= MessageChain(
                    Image(base64=calendar_img),
                    Image(base64=news_img),
                    Plain("请收好，这是今日份的报纸哦")
                )
            )
    except:
        print("定时发送60秒看世界新闻 发送消息时错误")

# 管理员指令：
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[check_member(BOT.admin)],
        inline_dispatchers=[
            Twilight(
                UnionMatch(BOT.cmd_prefix),
                UnionMatch(['60秒新闻', '60秒看世界'])
            )
        ]
    )
)
@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        decorators=[check_friend(BOT.admin)],
        inline_dispatchers=[
            Twilight(
                UnionMatch(BOT.cmd_prefix),
                UnionMatch(['60秒新闻', '60秒看世界'])
            )
        ]
    )
)
async def send_news_img_admin(app: Ariadne, target: Friend | Group):
    news_img = await get_news_img()
    if type(news_img) == int:
        await app.send_message(
            target,
            MessageChain(
                Plain(f"err-or发生{news_img}")
            )
        )
    else:
        await app.send_message(
            target,
            MessageChain(
                Image(base64=news_img),
                Plain("请收好，这是今日份的报纸哦")
            )
        )