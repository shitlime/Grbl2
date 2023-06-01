#!/usr/bin/python3
# -*- coding: utf-8 -*-

from asyncio.events import AbstractEventLoop

from bot_init import BOT
from modules.base.check import check_friend
from modules.base.message_queue import MessageQueue

from graia.saya import Saya
from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config, HttpClientConfig, WebsocketClientConfig
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne.event.lifecycle import ApplicationLaunched, ApplicationShutdowned


saya = Ariadne.create(Saya)

app = Ariadne(
    config(
        BOT.ariadne_config['qq_id'],  # 你的机器人的 qq 号
        BOT.ariadne_config['verify_key'],  # 填入 VerifyKey
        HttpClientConfig(BOT.ariadne_config['http_client_config']),
        WebsocketClientConfig(BOT.ariadne_config['ws_client_config']),
    ),
)

@app.broadcast.receiver("FriendMessage", decorators=[check_friend(BOT.admin)])
async def friend_message_listener(app: Ariadne, friend: Friend, message: MessageChain):
    friendMsg = message.display # type:str
    #print(friend.id) # 打印QQ号码
    if friendMsg == "|say h":
        await app.send_message(app, friend,
        MessageChain([Plain("Hello, World!")])
        )

@app.broadcast.receiver("GroupMessage", decorators=[MentionMe(BOT.info['name'])])
async def group_message_listener(app: Ariadne, group: Group, member: Member, message: MessageChain):
    message = message.display
    if "妈妈是谁" in message:
        await MessageQueue().send_message(
            app,
            group,
            MessageChain([Plain(BOT.info['author_info'])])
        )
    elif "爸爸是谁" in message or "主人是谁" in message:
        await MessageQueue().send_message(
            app,
            group,
            MessageChain([Plain("不知道哦")])
        )
    elif "在吗" in message:
        await MessageQueue().send_message(
            app,
            group,
            MessageChain([Plain("不在哦")])
        )

# 挂载消息中转
bg_tsk_1 = None
@app.broadcast.receiver(ApplicationLaunched)
async def start_background(loop: AbstractEventLoop):
    global bg_tsk_1
    if not bg_tsk_1:
        bg_tsk_1 = loop.create_task(MessageQueue().send_message_worker())

@app.broadcast.receiver(ApplicationShutdowned)
async def stop_background():
    global bg_tsk
    if bg_tsk:
        bg_tsk_1.cancel() # 取不取消随你, 但不要留到 Ariadne 生命周期外
        await bg_tsk_1
        bg_tsk_1 = None

# 加载saya模块
with saya.module_context():
    for m in BOT.modules:
        saya.require(m)

# 阻塞式启动
app.launch_blocking()
