import re
import asyncio

from bot_init import BOT
from graia.saya import Channel
from graia.scheduler import timers
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.scheduler.saya import SchedulerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain

from OutdatedAssetsException import OutdatedAssetsException
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

@channel.use(SchedulerSchema(timer=timers.crontabify("3 0 * * *")))
async def upload_trime_nightly(app: Ariadne):
    file_info = None
    while file_info is None:
        try:
            file_info = await get_all_file_info()
        except OutdatedAssetsException:
            asyncio.sleep(120)

    for file_name, file_url in file_info.items():
        data = await get_file_bytes(file_url)
        path_pattern = r"同文原版.+Nightly.+"
        name = file_name  + ".删后缀喵"
        for group_num in enable_group:
            group = await app.get_group(group_num)

            # 获取Trime Nightly存放的文件夹
            async for fi in app.get_file_iterator(target=group):
                if fi.is_directory == True and re.match(path_pattern, fi.name):
                    # 上传文件
                    await app.upload_file(
                        data=data,
                        target=group,
                        path=fi.path,
                        name=name)
                    print(f"{file_name}上传完成")
                    break
