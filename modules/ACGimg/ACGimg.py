import asyncio

from bot_init import BOT
from ..base.check import check_frequency
from .get_acg_img import get_acg_img

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.util.cooldown import CoolDown
from graia.ariadne.model import Group, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.event.message import GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import(
    Twilight,
    WildcardMatch,
    UnionMatch,
    FullMatch,
)

channel = Channel.current()
channel.name("ACG图片")
channel.author("Shitlime")
channel.description("""
ACG图片模块

功能：发送ACG图片
（AI画图无法使用时期的产物/代替品）
""")
#读取配置
config = BOT.get_modules_config('ACGimg')

#配置：
#启动词：
key_words = ['二次元图片', '二次元', '②', '二次元圖片']
#冷却时间：
#公共冷却：
cool_down_time = config['cool_down_time']
#频率表：
fqc_dict = {}
#个人冷却：
fqc_time = config['fqc_time']

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[check_frequency(fqc_dict, fqc_time), MentionMe()],
        inline_dispatchers=[
            CoolDown(cool_down_time),
            Twilight(
                WildcardMatch(),
                UnionMatch(key_words),
                WildcardMatch(),
            )
        ]
    )
)
async def acg_img(app: Ariadne, group: Group, member: Member):
    img = await get_acg_img()
    print("acgimg: 正在返回图片")
    if type(img) == bytes:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Image(base64=img),
                Plain('你要的图片')
            )
        )
    else:
        msg1 = await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(f' err-or发生{img}…'),
                Plain('\n冷却ing…')
            )
        )
        await asyncio.sleep(cool_down_time)
        await app.recall_message(msg1)