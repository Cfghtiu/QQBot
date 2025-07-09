import pkgutil
import importlib

from mirai import GroupMessage

from Bot import bot
from config import bot_config
from tools import equal


@bot.on(GroupMessage)
@equal("//reload")
async def run(event: GroupMessage):
    if event.sender.id == bot_config.owner:
        import config
        for i, name, is_pkg in pkgutil.iter_modules(config.__path__, config.__name__ + "."):
            module = importlib.import_module(name)
            importlib.reload(module)
        return bot.send(event, "OK!")
