from datetime import datetime, timezone

from bot_init import BOT
from ..base.check import check_member

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group, Member, MemberPerm
from graia.ariadne.message.element import Source
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import(
    Twilight,
    UnionMatch,
    RegexMatch,
    RegexResult,
    SpacePolicy
)

channel = Channel.current()
channel.name("撤回消息")
channel.description("""
让Bot撤回自己已经发送的消息
由于只有群组消息才有必要撤回，这里特指群组消息
""")

# 配置：
key_word = ["remsg", "recall message", "撤回"]

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[check_member(BOT.admin)],
        inline_dispatchers=[
            Twilight(
                UnionMatch(BOT.cmd_prefix),
                UnionMatch(key_word).space(SpacePolicy.FORCE),
                "num" << RegexMatch(r"[1-9]|[1-3][0-9]", optional=True)
            )
        ]
    )
)
async def recall_message(app: Ariadne, group: Group, source: Source, num: RegexResult):
    try:
        if num.result:
            num = int(num.result.display)
        else:
            num = 1
        # 从收到的命令消息开始遍历
        search_msg_id = source.id - 1
        msg = await app.get_message_from_id(search_msg_id, target=group)
        while num > 0:
            # 如果是Bot自己发送
            if msg.sender.id == BOT.ariadne_config["qq_id"]:
                # 如果消息已经超过2分钟，一般无法撤回
                if (datetime.now(timezone.utc) - msg.source.time).total_seconds() > 120:
                    print("Bot最近的消息已经超过2分钟")
                    # 如果Bot是群主/管理员，继续撤回
                    if (msg.sender.permission == MemberPerm.Administrator
                        or
                        msg.sender.permission == MemberPerm.Owner):
                        print(f"使用管理员权限撤回msg={msg}")
                        await app.recall_message(msg)
                    else:
                        print("Bot无管理员权限，撤回失败")
                        await app.send_message(group, MessageChain("消息超过2分钟且无权限撤回"))
                        return
                print(f"尝试撤回msg{msg}")
                await app.recall_message(msg)
                num -= 1
            # 撤回后寻找下一条消息
            search_msg_id -= 1
            msg = await app.get_message_from_id(search_msg_id, target=group)
    except:
        await app.send_message(
            group,
            MessageChain("指令执行未完成，可能有错误")
        )