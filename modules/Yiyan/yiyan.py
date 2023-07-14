from datetime import datetime

from modules.base.message_queue import MessageQueue

from bot_init import BOT
from .get_yiyan import get_yiyan, get_page_url

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Friend, Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, ForwardNode, Forward
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.ariadne.message.parser.twilight import(
    Twilight,
    UnionMatch,
    WildcardMatch,
    RegexMatch,
    RegexResult,
    SpacePolicy
)

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
# =====触发机制=====
#好友发送消息
get_f = ["|yy", "一言"]
#群里提到、@机器人
get_g = ["一言", "yiyan"]

# =====高级选项=====
# 句子类型  -类型|st
yiyan_type = {'动画': 'a', '漫画': 'b', '游戏': 'c', '文学': 'd',
'原创': 'e', '网络': 'f', '其他': 'g', '影视': 'h', '诗词': 'i',
'网易云': 'j', '哲学': 'k', '抖机灵': 'l'}


#消息响应：
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MentionMe(BOT.info['name'])],
        inline_dispatchers=[
            Twilight(
                WildcardMatch(),
                UnionMatch(get_g),
                "yiyan_type_cn" << RegexMatch(f"({'|'.join(list(yiyan_type.keys()))})?( {'| '.join(list(yiyan_type.keys()))})*"),
                "full_info" << RegexMatch("(高级|\-f)?"),
                "show_help" << RegexMatch("(帮助|\-h)?")
            )
        ]
    )
)
@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        inline_dispatchers=[
            Twilight(
                UnionMatch(get_f),
                "yiyan_type_cn" << RegexMatch(f"({'|'.join(list(yiyan_type.keys()))})?( {'| '.join(list(yiyan_type.keys()))})*"),
                "full_info" << RegexMatch("(高级|\-f)?"),
                "show_help" << RegexMatch("(帮助|\-h)?")
            )
        ]
    )
)
async def yiyan(app: Ariadne, target: Group | Friend, yiyan_type_cn: RegexResult, full_info: RegexResult, show_help: RegexResult):
    # deal with arguments
    #print(yiyan_type_cn)
    #print(type(yiyan_type_cn))
    yiyan_type_cn = yiyan_type_cn.result.display.split(' ')
    c = []
    if yiyan_type_cn != ['']:
        # select type
        for i in yiyan_type_cn:
            c.append(yiyan_type[i])
    else:
        # default: all type
        c = list(yiyan_type.values())
    full_info = full_info.result.display
    show_help = show_help.result.display

    # get yiyan
    yiyan_json = await get_yiyan(c, 'json', max_length=500)
    yiyan_text = yiyan_json['hitokoto']
    from_who, from_where = '', ''
    if yiyan_json['from_who']:
        from_who = yiyan_json['from_who']
    if yiyan_json['from']:
        from_where = yiyan_json['from']

    # send message
    # send full info
    if full_info:
        fwd_node_list = [
            ForwardNode(
                target=2854196306,
                time=datetime.now(),
                message=MessageChain(
                    Plain(f"{yiyan_text}\n\t——{from_who} {from_where}")
                ),
                name="【被夺舍】小冰",
            )
        ]
        fwd_node_list.append(
            ForwardNode(
                target=2854196306,
                time=datetime.now(),
                message=MessageChain(
                    Plain("Info：\n"),
                    Plain(str(yiyan_json).replace(', ', '\n'))
                ),
                name="【被夺舍】小冰",
            )
        )
        fwd_node_list.append(
            ForwardNode(
                target=2854196306,
                time=datetime.now(),
                message=MessageChain(
                    Plain("本条目的网址：\n"),
                    Plain(f"{get_page_url(yiyan_json['uuid'])}"),
                ),
                name="【被夺舍】小冰",
            )
        )
        await app.send_message(
            target,
            MessageChain(
                Forward(fwd_node_list)
            )
        )
    #send help
    elif show_help:
        await app.send_message(
            target,
            MessageChain(
                Plain("指令格式：\n"),
                Plain(f"一言 ({' '.join(list(yiyan_type.keys()))})? (高级)? (帮助)?")
            )
        )
    # default: send yiyan
    else:
        await app.send_message(
            target,
            MessageChain(
                Plain(f"{yiyan_text}\n\t——{from_who} {from_where}")
            )
        )