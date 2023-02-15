import re
import asyncio

from bot_init import BOT
from .char2image2 import char2image, fonts_loader
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

# fd_cache:
# 挂缓存，“二次元语录”渲染提速4秒🤣
fd_cache = [None, None]

# config
config = BOT.get_modules_config('break_tofu')
#说明： 字体文件来自 天珩全字库(TH-Tshyn)(http://cheonhyeong.com/Simplified/download.html)
#全字库路径
if BOT.sys == 'Windows':
    fonts_path = config['font_path_windows']
elif BOT.sys == 'Linux':
    fonts_path = config['font_path_linux']

# font config
fonts = {
# format:
# "info" : "font"

"ttc" : "TH-Times.ttc",
"P0" : "TH-Tshyn-P0.ttf",
"P1" : "TH-Tshyn-P1.ttf",
"P2" : "TH-Tshyn-P2.ttf",
"P16" : "TH-Tshyn-P16.ttf"
}

# 回复式豆腐块响应
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
    # DEBUG
    print(f"quote_message={quote_message}")
    print(f"type(qm)={type(quote_message)}")

    tofu = ''    # tofu默认为空字符串（在banText中）
    if type(quote_message) == Quote:
        tofu = quote_message.origin.display    # 得到quote的文本
    elif type(quote_message) == type(None):
        pass
    else:
        tofu = quote_message.message_chain.display    # 得到quote的文本

    # DEBUG
    #print(f"tofu={tofu}")

    if tofu not in banText:
        print(f"豆腐块:{tofu}")
        await app.send_message(
            group,
            MessageChain(Image(data_bytes= await get_tofu_img(tofu, fd_cache))),
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
    if tofu in banText:
        pass
    else:
        print(f"豆腐块cmd:{tofu}")
        await app.send_message(
            target,
            MessageChain(
                Plain(f"{tofu[:20]} : "),
                Image(data_bytes= await get_tofu_img(tofu, fd_cache))
                )
        )

# 渲染豆腐块
async def get_tofu_img(tofu: str, fd_cache: list):
    # 单行
    if len(tofu) > 26:
        if fd_cache[0] == None:
            #fd_oneline = fonts_loader(fonts, fonts_path, font_size)
            fd_cache[0] = await asyncio.to_thread(fonts_loader, fonts, fonts_path, 60)
        return await asyncio.to_thread(char2image, tofu, fonts_dict= fd_cache[0], offset= (100, 100, 70))
    # 多行
    else:
        if fd_cache[1] == None:
            #fd_multiline = fonts_loader(fonts, fonts_path, font_size)
            fd_cache[1] = await asyncio.to_thread(fonts_loader, fonts, fonts_path, 120)
        return await asyncio.to_thread(char2image, tofu, fonts_dict= fd_cache[1], offset= (10, 10, 10))
