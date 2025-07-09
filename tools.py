import base64
import io
import inspect
import pickle
from typing import Any
from functools import wraps
import atexit

from httpx import AsyncClient
from PIL import Image as PILImage
from mirai import GroupMessage, Image


__all__ = [
    "equal",
    "conforms",
    "to_img",
    "get_avatar",
    "async_client",
    "mark",
    "check",
    "save_data",
    "load_data",
    "on_exit"
]
async_client = AsyncClient()


def check(groups: list):
    def a(func):
        @wraps(func)
        async def f(event: GroupMessage):
            if groups is not None:
                if event.group.id not in groups:
                    return
            return await func(event)
        return f
    return a


def to_img(data: io.BytesIO) -> Image:
    b = base64.b64encode(data.getvalue())
    s = b.decode("utf-8")
    return Image(base64=s)


def equal(msg: str):
    """字符串后的消息与msg完全相符时调用"""
    def a(func):
        @wraps(func)
        async def f(event: GroupMessage):
            if str(event.message_chain).strip() == msg:
                return await func(event)
        return f
    return a


def _conforms(message, matches: list) -> bool:
    for match in matches:
        if isinstance(match, str):
            if str(message).strip() == match:
                return True
        elif isinstance(match, type):
            if isinstance(message, match):
                return True
        elif match == Any:
            return True
        elif message == match:
            return True
    return False


def conforms(*matches):
    """
    消息符合特定格式时调用
    """
    def a(func):
        @wraps(func)
        async def f(event: GroupMessage):
            message_chain = event.message_chain
            message_chain.pop(0)  # 删除Source
            for args in matches:
                if len(message_chain) == len(args):
                    for message, arg in zip(message_chain, args):
                        if not isinstance(arg, list):
                            arg = [arg]
                        if not _conforms(message,  arg):
                            break
                    else:
                        return await func(event, *message_chain)
        return f
    return a


async def get_avatar(qq: int) -> PILImage.Image:
    reqs = await async_client.get(f"http://q1.qlogo.cn/g?b=qq&nk={qq}&s=100")
    cache = io.BytesIO(reqs.content)
    return PILImage.open(cache)


def mark(func):
    """做好标记，当触发这个函数的消息被撤回时，对应消息也会撤回"""
    from plugins.撤回 import message

    @wraps(func)
    async def a(event: GroupMessage):
        msg_id = event.message_chain.source.id
        result = await func(event)
        if inspect.isawaitable(result):
            reply_id = await result
            message[msg_id] = reply_id
    return a


def save_data(plugin: str, data):
    with open(f"data/{plugin}.pkl", "wb") as f:
        pickle.dump(data, f)
    print("ok")


def load_data(plugin: str, default):
    try:
        with open(f"data/{plugin}.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        ...
    except Exception as e:
        print("load data error:" + str(e))
        return default


def on_exit(func):
    atexit.register(func)
