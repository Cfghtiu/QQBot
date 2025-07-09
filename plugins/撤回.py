import logging
from Bot import bot
from mirai.models.events import GroupRecallEvent

logger = logging.getLogger(__name__)

message = {}


@bot.on(GroupRecallEvent)
async def run(event: GroupRecallEvent):
    reply_id = message.get(event.message_id, 0)
    if reply_id != 0:
        logger.info(f"撤回对应消息 msg {event.message_id} - rep {reply_id} ")
        return bot.recall(target=event.group.id, messageId=reply_id, sessionKey=bot.session)
