from config.bot_config import *
from mirai import Mirai, WebSocketAdapter

__all__ = [
    "bot",
    "run"
]

bot = Mirai(qq=qq, adapter=WebSocketAdapter(verify_key=verify_key, host=host, port=port))


def run():
    bot.run()
