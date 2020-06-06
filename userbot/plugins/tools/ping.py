from datetime import datetime
from userbot import userbot, Message


@userbot.on_cmd(
    "ping", about={'header': "check how long it takes to ping your userbot"}, group=-1)
async def pingme(message: Message):
    start = datetime.now()
    await message.edit('`Pong!`')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await message.edit(f"**P o n g !**\n`{m_s} ms`")
