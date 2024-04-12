import re

from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Friend
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import DetectSuffix
from graia.ariadne.event.message import FriendMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema


channel = Channel.current()
channel.meta["name"]="人工“智能”"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
价值1——的人工智能
谨慎使用，很有可能会与其他模块冲突

功能： “智能”回复好友消息
使用方法： 在saya中导入
saya.require("modules.AI")
"""

@channel.use(ListenerSchema(listening_events=[FriendMessage], decorators=[DetectSuffix(["?", "？", "吗", "呢"])]))
async def ai(app: Ariadne, friend: Friend, message: MessageChain):
    friend_msg = message.display
    friend_msg = re.sub("吗|呢", "", friend_msg)
    friend_msg = re.sub("\?", "!", friend_msg)
    friend_msg = re.sub("？", "！", friend_msg)
    await app.send_message(
        friend,
        MessageChain(f"{friend_msg}")
    )


from graiax.shortcut.saya import listen
from graiax.text2img.playwright import HTMLRenderer, convert_md, PageOption, ScreenshotOption

md = '''\
<div align="center">

# GraiaX TextToImage (Playwright)

*基于 Playwright 的适用于 Graia 的文转图工具*

</div>

GraiaX TextToImage (Playwright) 是一个基于 [GraiaX Playwright](https://github.com/GraiaCommunity/graiax-playwright) 的文转图工具，
其可以将纯文本、Markdown 文本、HTML 代码通过 Playwright 转换为图片。

## 安装

`pdm add graiax-text2img-playwright` 或 `poetry add graiax-text2img-playwright`。

> 我们强烈建议使用包管理器或虚拟环境
'''

@listen(FriendMessage)
async def function(app: Ariadne, friend: Friend):
    image_bytes = await HTMLRenderer().render(
        convert_md(md),
        extra_page_option=PageOption(viewport={"width": 840, "height": 10}, device_scale_factor=1.5),
        extra_screenshot_option=ScreenshotOption(type="jpeg", quality=80, scale="device"),
    )
    await app.send_message(friend, MessageChain(Image(data_bytes=image_bytes)))