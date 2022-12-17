import re
import os
import asyncio

from bot_init import BOT
from ..base.check import check_friend

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Friend
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.event.message import FriendMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import(
    Twilight,
    ElementMatch,
    FullMatch,
    UnionMatch,
    ParamMatch,
    ArgumentMatch,
    WildcardMatch,
    SpacePolicy,
    RegexResult
)

channel = Channel.current()
channel.name("获取机器ip")
channel.author("Shitlime")
channel.description("""
获取机器的ip地址

使用方法： 在saya中导入
saya.require("modules.get_ip")
""")

re_get_ipv6_linux = re.compile(r'inet6 ([0-9a-f:]+)')
re_get_ipv4_linux = re.compile(r'inet ([0-9\.]+)')
re_get_wlan_ip_addr_linux = re.compile(r'wlan0:(.+)', flags=re.DOTALL)

@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        decorators=[check_friend(BOT.admin)],
        inline_dispatchers=[
            Twilight(
                UnionMatch(BOT.cmd_prefix),
                FullMatch("ip").space(SpacePolicy.FORCE),
                "mode" << UnionMatch(["4", "v4", "6", "v6"])
            )
        ]
    )
)
async def get_ip(app: Ariadne, admin: Friend, mode: RegexResult):
    mode = mode.result.display
    if mode in ["4", "v4"]:
        s1 = await asyncio.to_thread(get_wlan_ip_addr)
        await app.send_message(
            admin,
            MessageChain(
                Plain("当前的地址为：\n"),
                Plain(get_ip_v4(s1)),
                Plain(" 喵~")
            )
        )
    else:
        s1 = await asyncio.to_thread(get_wlan_ip_addr)
        await app.send_message(
            admin,
            MessageChain(
                Plain("当前的地址为：\n"),
                Plain(get_ip_v6(s1)),
                Plain(" 喵~")
            )
        )

def get_ip_v4(s1):
    s2 = re_get_ipv4_linux.search(s1)
    s2 = s2.group(1)
    return s2

def get_ip_v6(s1):
    s2 = re_get_ipv6_linux.search(s1)
    s2 = s2.group(1)
    return s2

def get_wlan_ip_addr():
    s1 = os.popen("ip addr")
    s2 = re_get_wlan_ip_addr_linux.search(s1.read())
    s2 = s2.group(1)
    return s2