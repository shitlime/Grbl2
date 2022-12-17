import aiohttp

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Friend, Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
channel.name("一言")
channel.author("Shitlime")
channel.description("""
一言模块

功能： 获取一言并发送
使用方法： 在saya中导入
saya.require("modules.yiyan")
触发配置： 下方的get_f、get_g中输入
""")
#配置：
#好友发送消息
get_f = ["|yy", "一言"] #消息绝对相同才触发
#群里提到、@机器人
get_g = ["一言", "yiyan", "来点废话"] #消息里包含就触发

#消息响应：
@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def yiyan(app: Ariadne, friend: Friend, message: MessageChain):
    if message.display in get_f:
        await app.send_message(
            friend,
            MessageChain(f"{await get_text_yiyan()}")
        )

@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MentionMe()]))
async def yiyan(app: Ariadne, group: Group, message: MessageChain):
    for m in get_g:
        if m in message:
            await app.send_message(
                group,
                MessageChain(f"{await get_text_yiyan()}")
            )

#获取一言：
async def get_text_yiyan():
    url_yiyan = 'https://v1.hitokoto.cn/?c=a&b&c&d&f&i&k=c?&encode=text'
    async with aiohttp.ClientSession() as session:
        async with session.get(url_yiyan) as r:
            text = await r.read()
    return text.decode("utf-8")