# 发送消息用的中转站
# 2023-06-01 Shitlime： 为了躲避风控，需要收集全局的消息发送，并进行排队延时

import asyncio

import random

from graia.ariadne.app import Ariadne

# 全局延时
msg_delay = 26  # 上次稳定在：26

class MessageQueue:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.queue = asyncio.Queue()
        return cls.__instance
    
    async def send_message_worker(self):
        print(f"消息队列开始工作，当前延时{msg_delay}秒")
        while True:
            # 从消息队列中取出待发送的消息
            app, target, message, quote = await self.queue.get()
            try:
                mask = ''.join([ chr(random.randint(0x100000, 0x10FFFD)) for i in range(random.randint(20, 70)) ])
                mid = int(len(mask) / 2)
                await app.send_message(target, 
                                       mask[:mid] + '\n'
                                       + message + '\n'
                                       + mask[mid:])
            except Exception as e:
               print(f"ERROR: {e}")
            await asyncio.sleep(msg_delay)

    async def send_message(self, app: Ariadne, target, message, *, quote = False,):
        # 将待发送的消息添加到队列中
        await self.queue.put((app, target, message, quote,))
    
    # 如果可能，修改昵称

