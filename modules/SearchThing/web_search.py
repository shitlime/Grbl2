from urllib.parse import quote
from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.parser.twilight import(
    Twilight,
    FullMatch,
    UnionMatch,
    ParamMatch,
    SpacePolicy,
    RegexResult
)

channel = Channel.current()
channel.name("网络搜索")
channel.author("Shitlime")
channel.description("""
网络搜索模块

功能：根据查找条件回复搜索引擎地址/搜索结果
使用方法：在saya中导入
saya.require("modules.web_search")
""")
#配置：
#命令配置：
#查找参数：
search_mode_list = ["m", "萌", "萌娘", "萌百", "萌娘百科",
"鸡", "小鸡", "小鸡词典",
"c", "中国搜索",
"百", "百度", "百度搜索",
"searXNG", "搜索",
"bing", "必", "必应", "必应搜索"]
#查找链接配置：
url_moegirl = 'https://zh.moegirl.org.cn/index.php?search='
url_xiaoji = 'https://jikipedia.com/search?phrase='
url_baidu = 'https://www.baidu.com/s?ie=UTF-8&wd='
url_chinaso = 'https://www.chinaso.com/newssearch/all/allResults?q='
url_searxng = 'https://searx.fi/search?q='
url_bing = 'https://cn.bing.com/search?q='

#消息响应：
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage],
        inline_dispatchers=[
            Twilight(
                UnionMatch(["?", "？"]).space(SpacePolicy.PRESERVE),
                "search_mode" << UnionMatch(search_mode_list).space(SpacePolicy.FORCE),
                "search_string" << ParamMatch()
            )
        ]
    )
)
async def web_search(app: Ariadne, target: Group | Friend, search_mode: RegexResult, search_string: RegexResult):
    search_mode = search_mode.result.display
    search_string = search_string.result.display
    re_msg = None
    if search_mode in ["m", "萌", "萌娘", "萌百", "萌娘百科"]:
        search_string = quote(search_string)
        re_msg = MessageChain(Plain(url_moegirl + search_string))
    elif search_mode in ["鸡", "小鸡", "小鸡词典"]:
        search_string = quote(search_string)
        re_msg = MessageChain(Plain(url_xiaoji + search_string))
    elif search_mode in ["c", "中国搜索"]:
        search_string = quote(search_string)
        re_msg = MessageChain(Plain(url_chinaso + search_string))
    elif search_mode in ["searXNG", "搜索"]:
        search_string = quote(search_string)
        re_msg = MessageChain(Plain(url_searxng + search_string))
    elif search_mode in ["百", "百度", "百度搜索"]:
        search_string = quote(search_string)
        re_msg = MessageChain(Plain(url_baidu + search_string))
    elif search_mode in ["bing", "必", "必应", "必应搜索"]:
        search_string = quote(search_string)
        re_msg = MessageChain(Plain(url_bing + search_string))
    #发送消息
    if re_msg != None:
        await app.send_message(target, re_msg)
