from bot_init import BOT

from graia.saya import Saya
from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config, HttpClientConfig, WebsocketClientConfig
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Friend, Group, Member
from modules.base.check import check_friend
from graia.ariadne.util.cooldown import CoolDown

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
        await app.send_message(friend,
        MessageChain([Plain("Hello, World!")])
        )

@app.broadcast.receiver("GroupMessage", decorators=[MentionMe()])
async def group_message_listener(app: Ariadne, group: Group, member: Member, message: MessageChain):
    message = message.display
    if "妈妈是谁" in message:
        await app.send_message(group,
        MessageChain([Plain(BOT.info['author_info'])])
        )
    elif "爸爸是谁" in message or "主人是谁" in message:
        await app.send_message(group,
        MessageChain([Plain("不知道哦")])
        )
    elif "在吗" in message:
        await app.send_message(group,
        MessageChain([Plain("不在哦")])
        )

with saya.module_context():
    for m in BOT.modules:
        saya.require(m)

app.launch_blocking()
