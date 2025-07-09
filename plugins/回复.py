import logging
from mirai import GroupMessage
from config import reply_config, bot_config
from Bot import bot
from tools import check, mark

logger = logging.getLogger(__name__)


@bot.on(GroupMessage)
@mark
@check(bot_config.allow_groups)
async def run(event: GroupMessage):
    text = str(event.message_chain).strip()
    for key, value in reply_config.easy_map.items():
        if key == text:
            logger.info(f"{text} -> {value}")
            return bot.send(event, value)
