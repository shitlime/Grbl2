# 处理一些时间格式，转化成字符串
from datetime import datetime

def timestamp2str(timestamp: int) -> str:
    """
    时间戳转字符串

    timestamp: 时间戳

    Returns: 字符串的“年-月-日 时:分:秒”
    """
    return str(datetime.utcfromtimestamp(timestamp)).split('.')[0]