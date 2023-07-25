from graia.ariadne import Ariadne
from graia.ariadne.model import Group, Friend
from graia.ariadne.message.element import Quote

async def get_quote_message(message_id: int, target: Group | Friend):
    """
    message_id: 消息的id号
    target: 消息的目标

    Returns: 得到message_id为消息号的消息 所 回复的消息（得到回复的消息）
    """
    try:
        current_message = await Ariadne.current().get_message_from_id(message=message_id, target=target)
        # 判断quote是否为None
        if current_message.quote:
            quote_message = await Ariadne.current().get_message_from_id(message=current_message.quote.id, target=target)
            return quote_message
    except:
        print("get quote_message failed! return current_message's quote.")
        return current_message.quote