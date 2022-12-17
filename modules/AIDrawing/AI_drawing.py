import re
import base64
import asyncio
from urllib.parse import quote
from datetime import datetime

from bot_init import BOT
from ..base.check import check_frequency
from .get_ai_drawing_img import get_img_from_tags, get_img_from_img

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.util.cooldown import CoolDown
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At, Forward, ForwardNode, Quote
from graia.ariadne.message.parser.base import MentionMe
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.parser.twilight import(
    Twilight,
    WildcardMatch,
    UnionMatch,
    FullMatch,
    ElementMatch,
    RegexResult
)

channel = Channel.current()
channel.name("AI画图")
channel.author("Shitlime")
channel.description("""
AI画图模块

功能
1.画出自己的自画像
2.以tags画图
3.以图画图
""")
#读取配置
config = BOT.get_modules_config('AI_drawing')

#配置：
#API token：
token_list = config['token_list']
token = token_list[config['token_index']]
#Bot 的形象：
tags = config['bot_tags']
#冷却时间：
#公共冷却：
cool_down_time = config['cool_down_time']
#频率表：
fqc_dict = {}
#个人冷却（请求频率限制）:
fqc_time = config['fqc_time']

#不可使用的tags：
#ban_tags = ['loli', '1girl']
def get_ban_tags(file_path):
    f = open(file_path, 'r')
    l = f.read().split('\n')
    return l

if BOT.sys == 'Windows':
    file_path = "modules\\AIDrawing\\BanTags.txt"
elif BOT.sys == 'Linux':
    file_path = "modules/AIDrawing/BanTags.txt"
print('装载AI画图ban_tags…')
ban_tags = get_ban_tags(file_path)
print('装载完成！')


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[check_frequency(fqc_dict, fqc_time), MentionMe()],
        inline_dispatchers=[
            CoolDown(cool_down_time),
            Twilight(
                WildcardMatch(),
                FullMatch("画自己"),
                WildcardMatch(),
            )
        ]
    )
)
async def draw_me(app: Ariadne, group: Group, member: Member):
    #img = await asyncio.to_thread(get_img_from_tags, token, tags)
    img = await get_img_from_tags(token, tags)
    print("正在画画…")
    await app.send_message(
        group,
        MessageChain(
            At(target=member.id),
            Plain('拿起了画笔  :3')
        )
    )
    if img == None:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain('喵呀！被不可名状的错误吓到打翻了颜料瓶…')
            )
        )
    elif type(img) == int:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(f' err-or发生{img}…')
                )
        )
    else:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Image(base64= img)
            )
        )


# = = = = = tags画图 = = = = =

@ channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[check_frequency(fqc_dict, fqc_time), MentionMe()],
        inline_dispatchers=[
            CoolDown(cool_down_time),
            Twilight(
                WildcardMatch(),
                UnionMatch(["画画", "画一个", "画一个：", "畫一個", "畫畫"]),
                "tags"<< WildcardMatch(),
            )
        ]
    )
)
async def draw_by_tags(app: Ariadne, group: Group, member: Member, tags: RegexResult):
    global AID_PREV_TIME
    AID_PREV_TIME = datetime.now()
    tags = tags.result.display
    if tags_checker(tags):
        tags = quote(tags)
        print("正在画画…")
        b_msg1 = await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(' 拿起了画笔  :3')
            )
        )
        #img = await asyncio.to_thread(get_img_from_tags, token, tags)
        get_img_count = 0
        img = None
        while type(img) != bytes and get_img_count < 5:
            img = await get_img_from_tags(token, tags)
            get_img_count += 1
        print(f'tags={tags}')
        if img == None:
            await app.send_message(
                group,
                MessageChain(
                    At(target=member.id),
                    Plain(' 喵呀！被不可名状的错误吓到打翻了颜料瓶…')
                )
            )
        elif type(img) == int:
            await app.send_message(
                group,
                MessageChain(
                    At(target=member.id),
                    Plain(f' err-or发生{img}…')
                )
            )
        else:
            fwd_node_list = [
                ForwardNode(
                    target=member,
                    time=datetime.now(),
                    message=MessageChain(
                        Image(base64 = img)
                    ),
                    name=f"“{member.name}”的绘制结果",
                )
            ]
            fwd_node_list.append(
                ForwardNode(
                    target=member,
                    time=datetime.now(),
                    message=MessageChain(
                        Plain("绘制结果↑")
                    ),
                    name=f"“{member.name}”的绘制结果",
                )
            )
            fwd_node_list.append(
                ForwardNode(
                    target=member,
                    time=datetime.now(),
                    message=MessageChain(
                        Plain("信息:"),
                        Plain("\n----------\n"),
                        Plain(f"URL encode tags=\n{tags}"),
                        Plain("\n----------\n"),
                        Plain(f"请求者：\n{member.name}"),
                        Plain("\n----------\n"),
                        Plain(f"当前时间：\n{str(datetime.now()).split('.')[0]}"),
                        Plain("\n----------\n"),
                        Plain(f"注意⚠️\n个人冷却时间{fqc_time}秒\n"),
                        Plain(f"公共冷却时间{cool_down_time}秒\n"),
                        Plain("该时间内不会再接受同类请求"),
                        Plain("\n----------\n"),
                        Plain("一次请求多张功能开发中……其他信息：暂时没想好")
                    ),
                    name=f"“{member.name}”的绘制结果",
                )
            )
            await app.send_message(
                group,
                MessageChain(Forward(fwd_node_list))
            )
            #await app.recall_message(b_msg1)
            b_msg2 = await app.send_message(
                group,
                MessageChain(
                    At(target=member.id),
                    Plain(" ↑画完了，请收查↑\n"),
                    Plain("进入冷却…")
                )
            )
            await asyncio.sleep(cool_down_time)
            #await app.recall_message(b_msg2)
    else:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(' 含有不支持的tag')
            )
        )


# = = = = = 以图生图 = = = = =
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[check_frequency(fqc_dict, fqc_time)],
        inline_dispatchers=[
            CoolDown(cool_down_time),
            Twilight(
                UnionMatch(["以图画图", "以圖画圖", "以图绘图", "以图生图"]),
                WildcardMatch(),
                "i_img" << ElementMatch(Image)
            )
        ]
    )
)
async def draw_by_img(app: Ariadne, group: Group, member: Member, i_img: Image):
    i_img = await i_img.get_bytes()
    i_img = base64.b64encode(i_img)
    print("正在画画…")
    b_msg1 = await app.send_message(
        group,
        MessageChain(
            At(target=member.id),
            Plain(' 拿起了画笔  :3')
        )
    )
    get_img_count = 0
    r_img = None
    while type(r_img) != bytes and get_img_count < 5:
        r_img = await get_img_from_img(token, i_img)
        get_img_count += 1
    print("画完了")
    if r_img == None:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(' 喵呀！被不可名状的错误吓到打翻了颜料瓶…')
            )
        )
    elif type(r_img) == int:
        await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(f' err-or发生{r_img}…')
            )
        )
    else:
        fwd_node_list = [
            ForwardNode(
                target=member,
                time=datetime.now(),
                message=MessageChain(
                    Image(base64=r_img)
                ),
                name=f"“{member.name}”的以图绘图",
            )
        ]
        fwd_node_list.append(
            ForwardNode(
                target=member,
                time=datetime.now(),
                message=MessageChain(
                    Plain("以图绘图结果↑")
                ),
                name=f"“{member.name}”的以图绘图",
            )
        )
        fwd_node_list.append(
            ForwardNode(
                target=member,
                time=datetime.now(),
                message=MessageChain(
                    Plain("信息:"),
                    Plain("\n----------\n"),
                    Plain("原图：\n"),
                    Image(base64=i_img),
                    Plain("\n----------\n"),
                    Plain(f"请求者：\n{member.name}"),
                    Plain("\n----------\n"),
                    Plain(f"当前时间：\n{str(datetime.now()).split('.')[0]}"),
                    Plain("\n----------\n"),
                    Plain(f"注意⚠️\n个人冷却时间{fqc_time}秒\n"),
                    Plain(f"公共冷却时间{cool_down_time}秒\n"),
                    Plain("该时间内不会再接受同类请求"),
                    Plain("\n----------\n"),
                    Plain("其他信息：暂时没想好")
                ),
                name=f"“{member.name}”的以图绘图",
            )
        )
        await app.send_message(
            group,
            MessageChain(Forward(fwd_node_list))
        )
        #await app.recall_message(b_msg1)
        b_msg2 = await app.send_message(
            group,
            MessageChain(
                At(target=member.id),
                Plain(" ↑画完了，请收查↑\n"),
                Plain("进入冷却…")
            )
        )
        await asyncio.sleep(cool_down_time)
        #await app.recall_message(b_msg2)




# = = = = = 函数 = = = = =

def tags_checker(tags: str):
    if tags[-1] != ',':
        tags += ','
    tag_like = re.compile(r'[\{\(]*(.+?)[\}\)]*, ?')
    ban_char = re.compile(r"[^a-zA-Z0-9 _\-/\(\):'&;\{\}]")
    tag_list = tag_like.findall(tags)
    for t in tag_list:
        if t in ban_tags:
            print(f"不合法的tag: {t}")
            return False
        if ban_char.search(t):
            print(f"不合法字集的tag: {t}")
            return False
    return True
