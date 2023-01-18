from bot_init import BOT
from ..base.check import check_group

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Member, Group
from graia.ariadne.model.relationship import MemberPerm
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.event.mirai import GroupNameChangeEvent, MemberCardChangeEvent, MemberSpecialTitleChangeEvent
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
channel.name("群内资料改变时动作")
channel.author("Shitlime")
channel.description("""
群名称改变时Bot的动作

功能：群名称改变时会发送消息
""")

config = BOT.get_modules_config("InfosChange")

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

# 群成员昵称被群主/管理员改变
@channel.use(
    ListenerSchema(
        listening_events=[MemberCardChangeEvent],
        decorators=[check_group(enable_group)]
    )
)
async def memberCardChangeAction(app: Ariadne, group: Group, event: MemberCardChangeEvent):
    # 在修改者为群主/管理员，且被修改者不为群主/管理员自己时触发
    if event.operator == None:
        # 没有捕获到操作者信息时不做任何动作
        return
    if (
        (event.operator.permission == MemberPerm.Owner
        or event.operator.permission == MemberPerm.Administrator)
        and
        event.member != event.operator
    ):
        await app.send_group_message(
            group,
            MessageChain(
                Plain(f"{event.operator.name} 悄悄把 {event.origin} 的名片改成了 {event.current}")
            )
        )

# 群成员获得群主授予的头衔
@channel.use(
    ListenerSchema(
        listening_events=[MemberSpecialTitleChangeEvent],
        decorators=[check_group(enable_group)]
    )
)
async def memberSpecialTitleChangeAction(app: Ariadne, group: Group, event: MemberSpecialTitleChangeEvent):
    await app.send_group_message(
        group,
        MessageChain(
            Plain(f"恭喜！ {event.member} 的头衔由 {event.origin} 被群主更新为 {event.current}")
        )
    )