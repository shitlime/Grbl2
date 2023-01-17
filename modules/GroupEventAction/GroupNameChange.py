from bot_init import BOT
from ..base.check import check_group

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Member, Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.event.mirai import GroupNameChangeEvent
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
channel.name("群名改变时动作")
channel.author("Shitlime")
channel.description("""
群名称改变时Bot的动作

功能：群名称改变时会发送消息
""")

config = BOT.get_modules_config("GroupNameChange")

# 配置：配置启用本功能的群
enable_group = config["enable_group"]    # list

# 群名称变化
@channel.use(
    ListenerSchema(
        listening_events=[GroupNameChangeEvent],
        decorators=[check_group(enable_group)]
    )
)
async def groupNameChangeAction(app: Ariadne, group: Group, operator: Member, event: GroupNameChangeEvent):
    await app.send_group_message(
        group,
        MessageChain(
            Plain(f"{operator.name}修改了群名称\n"),
            Plain(f"群名称由{event.origin}变成了{event.current}")
        )
    )