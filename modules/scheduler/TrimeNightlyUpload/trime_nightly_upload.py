import datetime

from bot_init import BOT
from graia.saya import Channel
from graia.scheduler import timers
from graia.ariadne.app import Ariadne
from graia.scheduler.saya import SchedulerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain

from .get_trime_nightly import get_all_file_info, get_file_bytes

channel = Channel.current()
channel.meta["name"]="同文每夜构建"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
定时上传trime nightly build
"""

config = BOT.get_modules_config("TrimeNightlyUpload")

# 配置：
enable_group = config["enable_group"]    # list

@channel.use(SchedulerSchema(timer=timers.crontabify("11 0 * * *")))
async def upload_trime_nightly(app: Ariadne):
    file_info = await get_all_file_info()
    for file_name, file_url in file_info:
        data = await get_file_bytes(file_url)
        path = f"同文原版（Nightly Build，每夜版）{datetime.datetime.today()}"
        name = file_name + ".删后缀喵"
        for group_num in enable_group:
            await app.upload_file(
                data=data,
                target=group_num,
                path=path,
                name=name)