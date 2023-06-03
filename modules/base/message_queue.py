# 发送消息用的中转站
# 2023-06-01 Shitlime： 为了躲避风控，需要收集全局的消息发送，并进行排队延时

import asyncio

from graia.ariadne.app import Ariadne

# 全局延时
msg_delay = 12

class MessageQueue:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.queue = asyncio.Queue()
        return cls.__instance
    
    async def send_message_worker(self):
        print("消息队列开始工作")
        while True:
            # 从消息队列中取出待发送的消息
            app, target, message, quote = await self.queue.get()
            try:
                await app.send_message(target, message)
            except Exception as e:
               print(f"ERROR: {e}")
            await asyncio.sleep(msg_delay)

    async def send_message(self, app: Ariadne, target, message, *, quote = False,):
        # 将待发送的消息添加到队列中
        await self.queue.put((app, target, message, quote,))
    
    # 如果可能，修改昵称

