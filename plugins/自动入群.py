import logging
from Bot import bot
from mirai.models import BotInvitedJoinGroupRequestEvent

logger = logging.getLogger(__name__)


@bot.on(BotInvitedJoinGroupRequestEvent)
async def run(event: BotInvitedJoinGroupRequestEvent):
    logger.info("同意入群 %s(%d)", event.group_name, event.group_id)
    await bot.allow(event)
