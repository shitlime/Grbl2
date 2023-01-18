from bot_init import BOT
from ..base.check import check_group
from ..base.time2str import timestamp2str

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Member, Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At
from graia.ariadne.event.mirai import MemberLeaveEventQuit, MemberJoinEvent
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
channel.name("群成员加入/离开时动作")
channel.author("Shitlime")
channel.description("""
群成员加入/离开时Bot的动作

功能：群成员加入/离开时会发送消息
""")

config = BOT.get_modules_config("MemberJoinLeave")

# 配置：配置启用该功能的群
enable_group = config["enable_group"]    # list

# 群员离开：
@channel.use(
    ListenerSchema(
        listening_events=[MemberLeaveEventQuit],
        decorators=[check_group(enable_group)]
    )
)
async def memberLeaveAction(app: Ariadne, member: Member):
    st = Plain("")
    if member.special_title not in [None, ""]:
            st = Plain(f"Ta曾拥有{member.special_title}称号，代表了群内的功绩\n")
    await app.send_group_message(
        member,
        MessageChain(
            Image(data_bytes = await member.get_avatar()),
            Plain(f"{member.name}离开了我们\n"),
            Plain(f"Ta在{timestamp2str(member.join_timestamp)}加入本群，"),
            Plain(f"最后的发言时间是{timestamp2str(member.last_speak_timestamp)}\n"),
            st,
            Plain(f"希望Ta能找到新的归属")
        )
    )

# 新成员：
@channel.use(
    ListenerSchema(
        listening_events=[MemberJoinEvent],
        decorators=[check_group(enable_group)]
    )
)
async def memberJoinAction(app: Ariadne, member: Member):
    await app.send_group_message(
        member,
        MessageChain(
            At(target=member),
            Plain(" 欢迎入群，希望大家能够友好相处")
        )
    )