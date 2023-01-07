from graia.ariadne import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.message.element import Quote

async def get_quote_origin(message_id: int, group: Group) -> Quote:
    """
    message_id: 消息的id号
    group: 群号

    Returns: 得到message_id为消息号的消息 所 回复的消息（得到回复的消息）
    """
    try:
        quote_message = await Ariadne.current().get_message_from_id(message=message_id, target=group)
        return quote_message.quote
    except:
        print("get_quote_origin failed!")