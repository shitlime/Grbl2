from .get_yiyan import get_yiyan

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.parser.base import MentionMe, ContainKeyword
from graia.ariadne.model import Friend, Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.ariadne.message.parser.twilight import Twilight, UnionMatch, WildcardMatch

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
get_g = ["一言", "yiyan", "来点废话", "来点骚话"] #消息里包含就触发

#消息响应：
@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        inline_dispatchers=[
            Twilight(
                UnionMatch(get_f)
            )
        ]
    )
)
async def yiyan_friend(app: Ariadne, friend: Friend, message: MessageChain):
    await app.send_message(
        friend,
        MessageChain(f"{await get_yiyan(['a'], 'text')}")
    )

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MentionMe()],
        inline_dispatchers=[
            Twilight(
                WildcardMatch(),
                UnionMatch(get_g)
            )
        ]
    )
)
async def yiyan_group(app: Ariadne, group: Group, message: MessageChain):
    await app.send_message(
        group,
        MessageChain(f"{await get_yiyan(['l'], 'text')}")
    )