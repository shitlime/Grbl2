import re
import asyncio

from bot_init import BOT
from ..base.check import check_single
from .guess_tofu_core import GuessTofu
from .char2image2 import char2image, fonts_loader, image2bytes

from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Group, Friend, Member
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, Quote, At, Source
from graia.ariadne.util.interrupt import FunctionWaiter
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import(
    Twilight,
    ElementMatch,
    FullMatch,
    UnionMatch,
    ParamMatch,
    WildcardMatch,
    SpacePolicy,
    RegexMatch,
    RegexResult
)

channel = Channel.current()
channel.name("猜豆腐块游戏")
channel.author("Shitlime")
channel.description("""
猜豆腐块游戏

说明： 字体文件来自 天珩全字库(TH-Tshyn)(http://cheonhyeong.com/Simplified/download.html)
""")

# ===== 全局变量 =====
# fd_cache:
# 挂缓存
fd_cache = [None, None]

# config
config = BOT.get_modules_config('guess_tofu')
#全字库路径
if BOT.sys == 'Windows':
    fonts_path = config['font_path_windows']
elif BOT.sys == 'Linux':
    fonts_path = config['font_path_linux']

# font config
fonts = {
# format:
# "info" : "font"

"ttc" : "TH-Times.ttc",
"P0" : "TH-Tshyn-P0.ttf",
"P1" : "TH-Tshyn-P1.ttf",
"P2" : "TH-Tshyn-P2.ttf",
"P16" : "TH-Tshyn-P16.ttf"
}

# 单例限制
playing = []
# TODO
# 计分板
scroes = {}
# ===== 全局变量end =====


# 猜豆腐块游戏-单
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage],
        inline_dispatchers=[
            Twilight(
                UnionMatch(['猜豆腐', '豆腐块游戏']),
                "level" << UnionMatch([str(i) for i in range(8) ]),
                "char_range" << RegexMatch(r"([0-9A-Fa-f]{1,8}-[0-9A-Fa-f]{1,8} ?)+", optional=True)
            )
        ],
        decorators=[check_single(playing)]
    )
)
async def guess_tofu(app: Ariadne, target: Group|Friend, level: RegexResult, char_range: RegexResult):
    # 根据参数生成猜豆腐实例
    level = int(level.result.display)
    if char_range.matched:
        char_range_list = []
        # 切分每个范围
        cr_list = str(char_range.result).split(' ')
        for cr in cr_list:
            # 切分开始、结束
            cr = str(cr).split('-')
            char_range_start = int(cr[0], 16)
            char_range_end = int(cr[1], 16)
        if (char_range_end >= char_range_start):
            # 范围[start, end)
            char_range_list.append((char_range_start, char_range_end))
        else:
            # 范围[end, start)
            char_range_list.append((char_range_end, char_range_start))
        gt = GuessTofu(level, char_range_list)
    else:
        gt = GuessTofu(level)
    gt.set_img(await get_tofu_img(gt.tofu, fd_cache))
    gt.masker()

    # 记录发送的提示性消息
    msg_list = []

    await app.send_message(
        target,
        MessageChain(
            Plain(f"【猜豆腐】-等级{level}\n"),
            Plain(f"规则：发送下图的文字\n"),
            Plain(f"注：超过1分钟未回应视为败北"),
            Image(
                data_bytes= await asyncio.to_thread(
                    image2bytes,
                    gt.img_masked
                )
            )
        )
    )

    async def waiter(events : GroupMessage | FriendMessage):
        if type(events.sender) == Member:
            # 是群消息
            waiter_target = events.sender.group
            # 记录玩家信息
            player = events.sender
        else:
            # 是好友消息
            waiter_target = events.sender
            # 记录玩家信息
            player = events.sender
        assert(type(waiter_target) != Member)
        # 判断是否为上下文中的target
        if waiter_target == target:
            # 取出消息内容
            answer = events.message_chain.display
            if len(answer) == 1:
                if answer == gt.tofu:
                    await app.send_message(
                        target,
                        MessageChain(
                            Plain(f'恭喜{player.name if type(player) is Member else player.nickname}'),
                            Plain(f' 答对了喵~↑\n'),
                            Plain(f'正确答案：【{gt.tofu}】'),
                            Image(
                                data_bytes= await asyncio.to_thread(
                                    image2bytes,
                                    gt.img
                                )
                            )
                        )
                    )
                    # 胜利的玩家
                    print(f" 胜利：{player}")
                    return 0    # 答对0
                else:
                    msg = await app.send_message(
                        target,
                        MessageChain(
                            Plain(player.name if type(player) is Member else player.nickname),
                            Plain('，很遗憾 不是这个喵~↓ '),
                            Plain('请继续猜喵~→')
                        )
                    )
                    msg_list.append(msg)
                    return 1    # 答错1
            elif answer in ['退出游戏', '结束游戏', '🏳️']:
                return -1    # 退出-1
            elif re.match(r'提示([1-9][0-9]?)$', answer):
                # 降低难度
                if len(answer) == 2:
                    gt.mask_rule_reduce2()
                    gt.masker()
                else:
                    for i in range(int(answer[2:])):
                        gt.mask_rule_reduce2()
                        gt.masker()
                msg = await app.send_message(
                    target,
                    MessageChain(
                        Plain('猜不出来吗？给你点提示喵~→'),
                        Image(
                            data_bytes= await asyncio.to_thread(
                                image2bytes,
                                gt.img_masked
                            )
                        )
                    )
                )
                msg_list.append(msg)
                return 2    # 降低难度2
    
    answer = None
    while answer != 0:
        answer = await FunctionWaiter(waiter, [GroupMessage, FriendMessage]).wait(timeout=60)
        if answer is None:
            await app.send_message(
                target,
                MessageChain(
                    Plain('哼 哼 时间到了喵~↑\n'),
                    Plain('由于没有猜出答案，覌白获得了胜利喵~↑\n'),
                    Plain(f'正确答案：【{gt.tofu}】'),
                    Image(
                        data_bytes= await asyncio.to_thread(
                            image2bytes,
                            gt.img
                        )
                    )
                )
            )
            break
        elif answer == -1:
            await app.send_message(
                target,
                MessageChain(
                    Plain('杂🐟 这么简单都猜不出来喵~↑\n'),
                    Plain('由于没有猜出答案，覌白获得了胜利喵~↑\n'),
                    Plain(f'正确答案：【{gt.tofu}】'),
                    Image(
                        data_bytes= await asyncio.to_thread(
                            image2bytes,
                            gt.img
                        )
                    )
                )
            )
            break
    # 撤回消息，减少对正常聊天的干扰
    for msg in msg_list:
        try:
            await app.recall_message(msg)
        except:
            pass
    # 删除猜豆腐对象
    del gt
    # 解除单例
    playing.remove(target)



# 渲染豆腐块
async def get_tofu_img(tofu: str, fd_cache: list):
    # 多行
    if len(tofu) > 26:
        if fd_cache[0] == None:
            fd_cache[0] = await asyncio.to_thread(fonts_loader, fonts, fonts_path, 60)
        return await asyncio.to_thread(char2image, tofu, fonts_dict= fd_cache[0], offset= (100, 100, 70))
    # 单行
    else:
        if fd_cache[1] == None:
            fd_cache[1] = await asyncio.to_thread(fonts_loader, fonts, fonts_path, 120)
        return await asyncio.to_thread(char2image, tofu, fonts_dict= fd_cache[1], offset= (5, 5, 5))
