import re
import datetime
import asyncio

from bot_init import BOT
from graia.saya import Channel
from graia.scheduler import timers
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.scheduler.saya import SchedulerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain

from .OutdatedAssetsException import OutdatedAssetsException
from .get_trime_nightly import get_info, get_file_bytes

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
    # 获取nightly build信息，每120s请求一次，最多60次
    all_info = None
    count = 1
    while all_info is None and count <= 60:
        try:
            all_info = await get_info()
        except OutdatedAssetsException as e:
            print(f"{e.message} 第{count}次 120s后重新获取")
            await asyncio.sleep(120)
        finally:
            count += 1

    # 上传到群文件
    file_info = all_info['assets']
    body = all_info['body']
    for file_name, file_url in file_info.items():
        # data = await get_file_bytes(file_url)
        # path_pattern = r"同文原版.+Nightly.+"
        # 重命名成 [日期]-[架构]-[commit次数]-[哈希]-[名称]-[r/d]
        regix_file_name = r"(trime-nightly)-(\d+)-g([a-f0-9]+)-(.+)-(release|debug).apk"
        file_name_groups = re.search(regix_file_name, file_name).groups()
        name = "{}月{}日-{}-{}个改动-{}-{}-{}.APK".format(
            datetime.datetime.now().month,    # 月
            datetime.datetime.now().day,      # 日
            file_name_groups[3],              # 架构
            file_name_groups[1],              # commit数
            file_name_groups[2],              # 哈希
            file_name_groups[0],              # 名称
            file_name_groups[4],              # release/debug
            )
        for group_num in enable_group:
            group = await app.get_group(group_num)
            if group == None:
                continue

            # 发送下崽链接
            await app.send_message(
                target=group,
                message=MessageChain(
                    Plain(f"{name} 下崽链接（建议复制使用浏览器打开）：\n"),
                    Plain(f"【GitHub】{file_url}\n"),
                    Plain(f"【代理加速】https://mirror.ghproxy.com/{file_url}")
                )
            )
