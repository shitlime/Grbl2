import re
import asyncio

from .char2image import char2image

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Group, Friend, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, Quote, At
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.parser.twilight import(
    Twilight,
    ElementMatch,
    FullMatch,
    UnionMatch,
    ParamMatch,
    WildcardMatch,
    SpacePolicy,
    RegexResult
)

channel = Channel.current()
channel.name("打碎豆腐块")
channel.author("Shitlime")
channel.description("""
打碎豆腐块
破解豆腐块

说明： 字体文件来自 天珩全字库(TH-Tshyn)(http://cheonhyeong.com/Simplified/download.html)

功能： 用全字库渲染豆腐块并发送
使用方法： 在saya中导入
saya.require("modules.break_tofu")
""")

# 配置
# 触发关键：
keyWord = ["豆腐块", "豆腐塊"]
# 不触发的文本：
banText = ['', '[图片]', '[语音]', '[视屏]']

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight(
                ElementMatch(At, optional=True),
                WildcardMatch(),
                UnionMatch(keyWord)
            )
        ]
    )
)
async def break_tofu(app: Ariadne, group: Group, message: MessageChain):
    # DEBUG
    #print(f"message={message}")

    tofu = ''
    try:
        quote = message.get(Quote)[0] # 得到quote
        tofu = quote.origin[0].display # 得到quote中的文本（豆腐块）
    except:
        print("获取quote失败")

    # DEBUG
    #print(f"tofu= {tofu}")
    #print(f"tofu type: {type(tofu)}")

    if tofu not in banText:
        print(f"豆腐块:{tofu}")
        await app.send_message(
            group,
            MessageChain(Image(data_bytes= await asyncio.to_thread(char2image, tofu)))
        )

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage],
        inline_dispatchers=[
            Twilight(
                UnionMatch(keyWord),
                "tofu" << WildcardMatch()
            )
        ]
    )
)
async def break_tofu_cmd(app: Ariadne, target: Group|Friend, tofu: RegexResult):
    tofu = tofu.result.display
    if tofu not in banText and len(tofu) <= 120:
        print(f"豆腐块cmd:{tofu}")
        await app.send_message(
            target,
            MessageChain(Image(data_bytes= await asyncio.to_thread(char2image, tofu)))
        )