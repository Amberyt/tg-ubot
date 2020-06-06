from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

from userbot import userbot, Message, Config, versions

LOGO_STICKER_ID, LOGO_STICKER_REF = None, None


@userbot.on_cmd("alive", about={'header': "This command is just for fun"})
async def alive(message: Message):
    await message.delete()
    try:
        if LOGO_STICKER_ID:
            await sendit(LOGO_STICKER_ID, message)
        else:
            await refresh_id()
            await sendit(LOGO_STICKER_ID, message)
    except (FileIdInvalid, FileReferenceEmpty, BadRequest):
        await refresh_id()
        await sendit(LOGO_STICKER_ID, message)
    output = f"""
**USERBOT is Alive!**

× **python version** : `{versions.__python_version__}`
× **pyrogram version** : `{versions.__pyro_version__}`
× **userbot version** : `{versions.__version__}`
× **repo** : [tg-ubot]({Config.UPSTREAM_REPO})

Type `.help` for more information!
"""
    await userbot.send_message(message.chat.id, output, disable_web_page_preview=True)


async def refresh_id():
    global LOGO_STICKER_ID, LOGO_STICKER_REF
    sticker = (await userbot.get_messages('tg_ubot', 4)).sticker
    LOGO_STICKER_ID = sticker.file_id
    LOGO_STICKER_REF = sticker.file_ref


async def sendit(fileid, message):
    await userbot.send_sticker(message.chat.id, fileid, file_ref=LOGO_STICKER_REF)
