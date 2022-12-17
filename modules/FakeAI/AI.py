import re

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Friend
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import DetectSuffix
from graia.ariadne.event.message import FriendMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema


channel = Channel.current()
channel.name("人工“智能”")
channel.author("Shitlime")
channel.description("""
价值1——的人工智能
谨慎使用，很有可能会与其他模块冲突

功能： “智能”回复好友消息
使用方法： 在saya中导入
saya.require("modules.AI")
""")

@channel.use(ListenerSchema(listening_events=[FriendMessage], decorators=[DetectSuffix(["?", "？", "吗", "呢"])]))
async def ai(app: Ariadne, friend: Friend, message: MessageChain):
    friend_msg = message.display
    friend_msg = re.sub("吗|呢", "", friend_msg)
    friend_msg = re.sub("\?", "!", friend_msg)
    friend_msg = re.sub("？", "！", friend_msg)
    await app.send_message(
        friend,
        MessageChain(f"{friend_msg}")
    )