import aiofiles

from userbot import userbot, Message


@userbot.on_cmd("logs", about={'header': "check userbot logs"})
async def check_logs(message: Message):
    """check logs"""
    await message.edit("`checking logs ...`")
    async with aiofiles.open("logs/userbot.log", "r") as l_f:
        await message.edit_or_send_as_file(f"**USERBOT LOGS** :\n\n`{await l_f.read()}`",
                                           filename='userbot.log',
                                           caption='userbot.log')
