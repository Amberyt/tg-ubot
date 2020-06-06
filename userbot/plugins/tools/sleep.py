import asyncio

from userbot import userbot, Message


@userbot.on_cmd("sleep (\\d+)", about={
    'header': "sleep userbot :P",
    'usage': "{tr}sleep [timeout in seconds]"})
async def sleep_(message: Message) -> None:
    seconds = int(message.matches[0].group(1))
    await message.edit(f"`sleeping {seconds} seconds...`")
    asyncio.get_event_loop().create_task(_slp_wrkr(seconds))


async def _slp_wrkr(seconds: int) -> None:
    await userbot.stop()
    await asyncio.sleep(seconds)
    await userbot.reload_plugins()
    await userbot.start()
