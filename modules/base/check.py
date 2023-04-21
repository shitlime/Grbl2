import asyncio
from datetime import datetime

from graia.ariadne import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Plain
from graia.ariadne.model import Friend, Group, Member
from graia.broadcast.exceptions import ExecutionStop
from graia.broadcast.builtin.decorators import Depend

# ===== 时间控制 =====
# 指令冷却(未实现)(废弃)
def get_delay(prev_time: datetime):
    sec = (datetime.now() - prev_time).seconds
    return sec

def cool_down(prev_time: datetime, second: int):
    """
    冷却\n
    prev_time 上一记录的时间\n
    second 延时的秒数\n
    """
    async def cool_down_time(app: Ariadne, target: Group | Friend):
        print(prev_time)
        if prev_time == None:
            return
        elif get_delay(prev_time) < second:
            await app.send_message(
                target,
                MessageChain(
                    Plain("指令冷却中")
                )
            )
            raise ExecutionStop
    return Depend(cool_down_time)

#限制响应频率：
def frequency(fqc_dict: dict, id: int):
    if fqc_dict.get(id): # 如果fqc_dict存在索引为id的项
        sec = get_delay(fqc_dict.get(id))
        return sec
    else:
        fqc_dict[id] = datetime.now()
        return -1

def check_frequency(fqc_dict: dict, max_frequency: int):
    """
    检查某群的成员的频率\n
    fqc_dict: {id: datetime}字典，储存所有请求者的请求时间，不同的指令可以使用不同的fqc字典实现不同的频率计数\n
    max_frequency: 允许的最大频率，单位：秒/次\n
    """
    async def check_frequency_deco(app: Ariadne, group: Group, member: Member):
        print(f"fqc_dict={fqc_dict}")
        fqc = frequency(fqc_dict, member.id)
        if fqc == -1:    # 第一次的请求
            return
        elif fqc < max_frequency:    # 违反频率的请求
            await app.send_message(
                group,
                MessageChain(
                    At(member.id),
                    Plain(f"你太快了喵！\n（{max_frequency - fqc}s）不能持久一点吗")
                    )
                )
            raise ExecutionStop
        else:    # 符合频率的请求
            fqc_dict[member.id] = datetime.now()
    return Depend(check_frequency_deco)

# ===== 目标控制 =====
#指定响应对象：
def check_friend(friends: list[int]):  #指定响应的好友
    async def check_friend_id(friend: Friend):
        if friend.id not in friends:
            raise ExecutionStop
    return Depend(check_friend_id)

def check_member(members: list[int]):  #指定响应的群成员
    async def check_member_id(member: Member):
        if member.id not in members:
            raise ExecutionStop
    return Depend(check_member_id)

def check_group(groups: list[int]):  #指定响应的群
    async def check_group_id(group: Group):
        if group.id not in groups:
            raise ExecutionStop
    return Depend(check_group_id)

# ===== 限制对话单例 =====
def check_single(log: list):
    async def check_single_deco(app: Ariadne, target: Group | Friend):
        if target in log:
            # 如果已经有进行中的实例，则做出提示
            await app.send_message(
                target,
                MessageChain("进行中…")
            )
            raise ExecutionStop
        else:
            # 如果没有进行中的实例，将本次验证的实例作为新实例
            log.append(target)
    return Depend(check_single_deco)
