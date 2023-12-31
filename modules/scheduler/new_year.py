from bot_init import BOT
from graia.saya import Channel
from graia.scheduler import timers
from graia.ariadne.app import Ariadne
from graia.scheduler.saya import SchedulerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain

channel = Channel.current()
channel.meta["name"]="定时发送新年好"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
新年好
"""

config = BOT.get_modules_config("new_year")

# 配置：
enable_group = config["enable_group"]    # list
enable_friend = config["enable_friend"]    # list

@channel.use(SchedulerSchema(timer = timers.crontabify("0 0 1 1 *")))
async def send_happy_new_year(app: Ariadne):
    msg = MessageChain(
                    Plain("新年快乐喵 :3")
                )
    try:
        for group_num in enable_group:
            await app.send_group_message(
                target=group_num,
                message= msg
            )
        for friend_num in enable_friend:
            await app.send_friend_message(
                target=friend_num,
                message= msg
            )
    except:
        print("定时发送消息错误")