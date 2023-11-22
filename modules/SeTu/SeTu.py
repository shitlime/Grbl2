import asyncio

from bot_init import BOT
from modules.base.message_queue import MessageQueue
from .create_setu import create_setu

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.util.cooldown import CoolDown
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne.message.element import Plain, Image
from graia.ariadne.message.parser.base import MentionMe, ContainKeyword
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import FriendMessage, GroupMessage

channel = Channel.current()
channel.meta["name"]="涩图"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
涩图模块·假

说明： 参考了Abot(https://github.com/djkcyl/ABot-Graia)

功能： 绘制涩图并发送（
使用方法： 在saya中导入
saya.require("modules.SeTu")
"""
#读取配置
config = BOT.get_modules_config('SeTu')
cool_down_time = config['cool_down_time']

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MentionMe(BOT.info['name']), ContainKeyword("涩图")],
        inline_dispatchers=[CoolDown(cool_down_time)]
    )
)
async def SeTu(app: Ariadne, group: Group):
    await app.send_message(
        group,
        MessageChain(Image(data_bytes= await asyncio.to_thread(create_setu)))
    )