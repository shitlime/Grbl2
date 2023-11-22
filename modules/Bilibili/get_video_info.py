from .video import get_video_info

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
                Plain(f"播放量：{info.get('stat').get('view')}\n"),
                Plain(f"收藏：{info.get('stat').get('favorite')}\n"),
                Plain(f"硬币：{info.get('stat').get('coin')}\n"),
                Plain(f"点赞：{info.get('stat').get('like')}\n"),
                Plain(f"投稿：{timestamp2str(info.get('pubdate'))}\n"),
                Plain(f"简介：{info.get('desc')}\n"),
                Plain(f"ID：{info.get('bvid')} av{info.get('aid')}\n")
            ),
        )