from .video import get_video_ai_conclusion

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
channel.meta["name"]="获取哔哩哔哩AI视频总结"
channel.meta["author"]="Shitlime"
channel.meta["description"]="""
根据BV号或av号，获取哔哩哔哩AI视频总结
"""

# ==== 配置 ====
keyword = ["AI总结", "ai总结", "aibl"]
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
async def get_video_ai_conclusion_quote(app: Ariadne, target: Group | Friend, source: Source):
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
    ai_conclusion = await get_video_ai_conclusion(string)

    # 取出总结、大纲
    summary = ""
    outline = []
    if ai_conclusion:
        summary = ai_conclusion['model_result']['summary']
        if ai_conclusion['model_result']['outline']:
            for i, part in enumerate(ai_conclusion['model_result']['outline']):
                outline.append(f"【{i+1}】{part['title']}")
        outline = '\n'.join(outline)

    # 发送消息
    if summary or outline:
        await app.send_message(
            target,
            MessageChain(
                Plain(f"【总结】{summary}\n"),
                Plain(f"{outline}\n")
            ),
        )
    else:
        await app.send_message(
            target,
            MessageChain(
                Plain(f"该视频没有AI总结喵~")
            ),
        )
