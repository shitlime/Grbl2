import re
import os
import math

from bot_init import BOT

from pypinyin import pinyin
from graia.saya import Channel
from graia.ariadne import Ariadne
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne.message.element import At, Plain
from graia.ariadne.message.chain import MessageChain
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
channel.name("字符查找")
channel.author("Shitlime")
channel.description("""
字符查找模块
（查字模块）

功能： 根据查找条件查找字符信息并回复
使用方法： 在saya中导入
saya.require("modules.search_char")
""")
#读取配置
config = BOT.get_modules_config('search_char')

#配置：
#命令配置：
#查找参数：
search_mode_list = ["g", "G", "观", "观星三拼", "s", "S", "四", "四角", "四角号码", "u", "U"]
#查字数据库配置：
#码表型
#名称：
dict_g_name = "tri_py_gxsp.dict-b2.yaml"
dict_s_name = "sjhm.dict-b1.yaml"

#共用路径(根据系统设置不同路径)：
if BOT.sys == 'Windows':
    dict_path = config['dict_path_windows']
elif BOT.sys == 'Linux':
    dict_path = dict_path = config['dict_path_linux']
#数据库型：
  #未来补上unicode pad数据库查找unicode信息

#消息响应：
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight(
                UnionMatch(["?", "？", "#"]).space(SpacePolicy.PRESERVE),
                "search_mode" << UnionMatch(search_mode_list).space(SpacePolicy.FORCE),
                "search_char" << ParamMatch()
            )
        ]
    )
)
async def search_char(app: Ariadne, member: Member, group: Group, search_mode: RegexResult, search_char: RegexResult):
    #print(f"sm：{search_mode.},sc:{search_char}")
    search_mode = search_mode.result.display
    search_char = search_char.result.display
    re_msg_u = ToUnicode(search_char)
    re_msg = None
    #查观星三拼
    if search_mode in ["g", "G", "观", "观星三拼"]:
        re_msg_u = ')('.join(re_msg_u)
        re_msg = MessageChain(
            At(target=member.id),
            Plain(f"【{search_char}】({re_msg_u})\n"),
            Plain(f"[观星三拼]{find_char(dict_g, search_char)}")
        )
    #查四角号码
    elif search_mode in ["s", "S", "四", "四角", "四角号码"]:
        re_msg_u = ')('.join(re_msg_u)
        re_msg = MessageChain(
            At(target=member.id),
            Plain(f"【{search_char}】({re_msg_u})\n"),
            Plain(f"[四角号码]{find_char(dict_s, search_char)}")
        )
        pass
    #以字查U码：
    elif search_mode in ["u"]:
        if len(search_char) == 1:
            re_msg_u = '】【'.join(re_msg_u)
        else:
            re_msg_u = re_msg_u
        re_msg = MessageChain(
            f"【{search_char}】【{re_msg_u}】"
        )
    #以U码查字：
    elif search_mode in ["U"]:
        re_msg_c = UnicodeTo(search_char)
        re_msg = MessageChain(
            f"【{search_char}】->【{re_msg_c}】"
        )
    #发送信息：
    if re_msg != None:
        await app.send_message(group, re_msg)

#查找字符信息：
#以下为查字模块部分
def readtxt(path: str, name: str, mode: str ='rb'):#读取文本文件
    f = open(os.path.join(path, name), mode)
    s = f.read().decode('utf-8')
    f.close()
    return s

def dict_change(dt_s: str):#字典处理
    d1 = dt_s.split('\n')
    d2 = {}
    while '' in d1:
        d1.remove('')
    for d11 in d1:
        if d11[0] == '#':
            continue
        d11 = d11.split('\t')
        if len(d11) == 1:
            continue
        if d11[0] in d2:
            d2[d11[0]].append(d11[1])
            continue
        d2[d11[0]] = [d11[1]]
    return d2

def load_dict(dict_path: str, dict_name: str):
    print("装载字典……")
    dt_s = readtxt(dict_path, dict_name)
    dt = dict_change(dt_s)
    print(f"{dict_name}装载完成！")
    return dt

def find_char(dt: dict, ch: str):
    tb = dt.get(ch)  #tb:table,码；ch:char,字符
    if tb == None:
        return '404 NOT FOUND 喵~'
    return '或'.join(tb)

#码表型字典数据装载：
dict_g = load_dict(dict_path, dict_g_name)#观星三拼
dict_s = load_dict(dict_path, dict_s_name)#四角号码

#以下为Unicode处理模块：
def ToUTF16(kw_num):#某些字用unicode转utf16
    H = str(hex(math.floor((kw_num-0x10000)/0x400)+0xd800)).replace('0x', '\\u')
    L = str(hex((kw_num - 0x10000) % 0x400 + 0xdc00)).replace('0x', '\\u')
    return H+L

def ToUnicode(kw: str):
    kw_l = len(kw)
    if kw_l == 1:
        dy = pinyin(kw, heteronym=True, errors='ignore')
        if len(dy) > 0:
            dy = '[%s]'%']['.join(dy[0])
        else:
            dy = None
        kw_num = ord(kw)
        kw_u = hex(kw_num).replace('0x', 'U+').upper()
        msg = '没有记录这个数据 喵~'
        if 0x0000 <= kw_num <= 0x007f:
            msg = 'C0控制符及基本拉丁文'
        if 0x0080 <= kw_num <= 0x00ff:
            msg = 'C1控制符及拉丁文补充'
        if 0x0100 <= kw_num <= 0x017f:
            msg = '拉丁文-扩展A'
        if 0x0180 <= kw_num <= 0x024f:
            msg = '拉丁文-扩展B'
        if 0x0250 <= kw_num <= 0x02af:
            msg = '国际音标扩展'
        if 0x02b0 <= kw_num <= 0x02ff:
            msg = '空白修饰字母'
        if 0x0300 <= kw_num <= 0x036f:
            msg = '结合用读音符'
        if 0x0370 <= kw_num <= 0x03ff:
            msg = '希腊文及科普特文'
        if 0x4e00 <= kw_num <= 0x9fff:
            msg = '汉字'
        if 0x3400 <= kw_num <= 0x4db5:
            msg = '汉字-扩展A区'
        if 0x9fcd <= kw_num <= 0x9fd5:
            msg = '急用汉字'
        if 0x00020000 <= kw_num <= 0x0002a6d6:
            msg = '汉字-扩展B区'
        if 0x0002a700 <= kw_num <= 0x0002b734:
            msg = '汉字-扩展C区'
        if 0x0002b740 <= kw_num <= 0x0002b81d:
            msg = '汉字-扩展D区'
        if 0x0002b820 <= kw_num <= 0x0002ceaf:
            msg = '汉字-扩展E区'
        if 0x0002ceb0 <= kw_num <= 0x0002ebef:
            msg = '汉字-扩展F区'
        if 0x00030000 <= kw_num <= 0x0003134a:
            msg = '汉字-扩展G区'
        if 0x000F0000 <= kw_num <= 0x0010ffff:
            msg = 'PUA'
        if len(kw_u) > 6:
            kw_u16 = ToUTF16(kw_num)
            if dy == None:
                return kw_u, msg, kw_u16
            return dy, kw_u, msg, kw_u16
        if dy == None:
            return kw_u, msg
        return dy, kw_u, msg
    else:
        kw_u = ''
        for s1 in kw:
            s1_num = ord(s1)
            s1_u = hex(s1_num).replace('0x', '\\u')
            if len(s1_u) > 6:
                s1_u = ToUTF16(s1_num)
            kw_u += s1_u
        return kw_u

def UnicodeTo(kw: str):
    kws = kw.lower().split('\\u')
    while '' in kws:
        kws.remove('')
    kws_o = ''
    for kw in kws:
        if re.match(r'^[0-9A-Fa-f]{1,8}$', kw) == None:
            return '请输入正确的Unicode'
        if len(kw) <= 4:
            while len(kw) < 4:
                kw = '0' + kw
            kw = '\\u' + kw
        elif len(kw) > 4:
            while len(kw) < 8:
                kw = '0' + kw
            kw = '\\U' + kw
        kws_o += kw
    kws_o = kws_o.encode().decode('unicode-escape')
    return kws_o
