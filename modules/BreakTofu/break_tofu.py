import re
import asyncio

from .char2image2 import char2image
from ..base.get_quote_message import get_quote_message

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Group, Friend, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, Quote, At, Source
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
# 豆腐块文本长度限制：
max = 120

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
async def break_tofu(app: Ariadne, group: Group, source: Source):
    quote_message = await get_quote_message(source.id, group)
    tofu = ''    # tofu默认为空字符串（在banText中）
    if type(quote_message) == Quote:
        tofu = quote_message.origin.display    # 得到quote的文本
    else:
        tofu = quote_message.message_chain.display    # 得到quote的文本

    # DEBUG
    #print(f"quote_message={quote_message}")
    #print(f"tofu={tofu}")

    if tofu not in banText:
        print(f"豆腐块:{tofu}")
        await app.send_message(
            group,
            MessageChain(Image(data_bytes= await get_tofu_img())),
            quote=source
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
    if len(tofu) > max:
        await app.send_message(
            target,
            MessageChain(Plain(f"请求超出长度限制({max})喵！"))
        )
    elif tofu in banText:
        pass
    else:
        print(f"豆腐块cmd:{tofu}")
        await app.send_message(
            target,
            MessageChain(
                Plain(f"{tofu[:20]} : "),
                Image(data_bytes= await get_tofu_img())
                )
        )

async def get_tofu_img(tofu: str):
    if len(tofu) > 26:
        return await asyncio.to_thread(char2image, tofu, offset= (100, 100, 70))
    else:
        return await asyncio.to_thread(char2image, tofu, fontsize= 120, offset= (10, 10, 10))
    