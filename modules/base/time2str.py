# 处理一些时间格式，转化成字符串
import pytz
from datetime import datetime

def timestamp2str(timestamp: int) -> str:
    """
    时间戳转字符串

    timestamp: 时间戳

    Returns: 字符串的“年-月-日 时:分:秒”
    """
    timezone = pytz.timezone("Asia/Shanghai")
    dt = datetime.fromtimestamp(timestamp, timezone)
    return dt.strftime("%Y-%m-%d %H:%M:%S")