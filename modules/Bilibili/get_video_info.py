from .video import get_video_info, get_video
from loguru import logger

from ..base.get_quote_message import get_quote_message
from ..base.time2str import timestamp2str

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Group, Friend
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At, Source, Quote
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import(
    Twilight,
    FullMatch,
    UnionMatch,
    ParamMatch,
    ElementMatch,
    WildcardMatch,
    SpacePolicy,
    RegexMatch,
    RegexResult
)

channel = Channel.current()
channel.meta["name"]="获取哔哩哔哩视频信息"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
根据BV号或av号，获取哔哩哔哩视频信息
"""

# ==== 配置 ====
keyword = ["解析", "bili"]
# ==== End ====


# 自动识别BV号
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage],
        inline_dispatchers=[
            Twilight(
                WildcardMatch(),
                "bvid" << RegexMatch(r"BV[0-9a-zA-Z]{10}"),
                WildcardMatch(),
            )
        ]
    )
)
async def get_video_info_auto(app: Ariadne, target: Group | Friend, bvid: RegexResult, msg: MessageChain):
    bvid = bvid.result.display
    logger.info(f"识别到消息中含有BV：{bvid}")
    # 获取视屏信息
    video = get_video(bvid)
    info = await video.get_info()
    if info:
        # 发送消息
        await app.send_message(
            target,
            MessageChain(
                Plain(f"标题：{info.get('title')}\n"),
                Image(url=info.get('pic')),
                Plain(f"up主：{info.get('owner').get('name')}\n"),
                Plain(f"分区：{info.get('tname')}\n"),
                Plain(f"播放量：{info.get('stat').get('view')}"),
                Plain(f"收藏：{info.get('stat').get('favorite')}\n"),
                Plain(f"硬币：{info.get('stat').get('coin')}"),
                Plain(f"点赞：{info.get('stat').get('like')}\n"),
                Plain(f"投稿：{timestamp2str(info.get('pubdate'))}\n"),
                Plain(f"简介：{info.get('desc')[:51]}\n"),
                Plain(f"ID： av{info.get('aid')}\n")
            ),
        )
        if msg.display != info.get('bvid'):
            await app.send_message(
                target,
                MessageChain(
                    Plain(f"{info.get('bvid')}")
                )
            )


# 回复式主动获取信息
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage],
        inline_dispatchers=[
            Twilight(
                ElementMatch(At, optional=True),
                WildcardMatch(),
                UnionMatch(keyword),
            )
        ]
    )
)
async def get_video_info_quote(app: Ariadne, target: Group | Friend, source: Source):
    # 得到原消息
    message = await Ariadne.current().get_message_from_id(source.id, target)
    # 检测是否带回复
    if message.quote:
        quote_message = await get_quote_message(source.id, target)
        # 获取文本
        if type(quote_message) == Quote:
            string = quote_message.origin.display    # 得到quote的文本
        elif type(quote_message) == type(None):
            return
        else:
            string = quote_message.message_chain.display    # 得到quote的文本
    else:
        return
    # 获取视屏信息
    info = await get_video_info(string)
    if info:
        # 发送消息
        await app.send_message(
            target,
            MessageChain(
                Plain(f"标题：{info.get('title')}\n"),
                Image(url=info.get('pic')),
                Plain(f"up主：{info.get('owner').get('name')}\n"),
                Plain(f"分区：{info.get('tname')}\n"),
                Plain(f"播放量：{info.get('stat').get('view')}"),
                Plain(f"收藏：{info.get('stat').get('favorite')}\n"),
                Plain(f"硬币：{info.get('stat').get('coin')}"),
                Plain(f"点赞：{info.get('stat').get('like')}\n"),
                Plain(f"投稿：{timestamp2str(info.get('pubdate'))}\n"),
                Plain(f"简介：{info.get('desc')}\n"),
                Plain(f"ID：{info.get('bvid')} av{info.get('aid')}\n")
            ),
        )