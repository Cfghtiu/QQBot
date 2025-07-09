import asyncio
import logging

import dashscope
from dashscope.api_entities.dashscope_response import Role, Message
from mirai import GroupMessage, At

from Bot import bot
from tools import mark, check, on_exit, save_data, load_data
from config import qianwen_config, bot_config

dashscope.api_key = qianwen_config.api_key

logger = logging.getLogger(__name__)
envs: dict[int, list] = load_data(__name__, {})
lock: dict[int, bool] = {}


@bot.on(GroupMessage)
@mark
@check(bot_config.allow_groups)
async def run(event: GroupMessage):
    self = str(At(bot.qq))
    text = str(event.message_chain)

    if text.startswith(self):
        if lock.get(event.group.id, False) is True:
            return bot.send(event, f"别急，我在思考")
        try:
            lock[event.group.id] = True
            prompt = text[len(self):].strip()
            messages = envs.setdefault(event.sender.group.id, [])
            logger.info(f"{event.group.id}:{event.sender.id} 调用AI: {prompt[:20]}...")

            resp = await asyncio.to_thread(
                dashscope.Generation.call,
                qianwen_config.model,
                prompt,
                messages=messages
            )
            if resp.status_code != 200:
                logger.error(f"{resp.status_code}, {resp.message}")
                return bot.send(event, f"AI出了点啸问题，请联系管理员修复")
            result = resp.output.text

            logger.info(f"{event.group.id}:{event.sender.id} -> {result[:20]}...({len(result)})")
            messages.append({"role": Role.USER, "content": prompt})
            messages.append({"role": Role.ASSISTANT, "content": prompt})

            if len(prompt) > qianwen_config.history_cache_size:
                messages.pop(0)
                messages.pop(0)
            return bot.send(event, result)
        finally:
            lock.pop(event.group.id, None)
    elif text == ".reset":
        envs.pop(event.sender.group.id, None)
        return bot.send(event, f"失忆完毕~")


@on_exit
def exit_():
    save_data(__name__, envs)
