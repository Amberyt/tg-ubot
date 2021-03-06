
import os
import time

from telegraph import upload_file

from userbot import userbot, Message, Config
from userbot.utils import progress

_T_LIMIT = 5242880


@userbot.on_cmd("telegraph", about={
    'header': "Upload file to Telegra.ph's servers",
    'types': ['.jpg', '.jpeg', '.png', '.gif', '.mp4'],
    'usage': "reply {tr}telegraph to supported media : limit 5MB"})
async def telegraph_(message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.err("reply to supported media")
        return
    if not ((replied.photo and replied.photo.file_size <= _T_LIMIT)
            or (replied.animation and replied.animation.file_size <= _T_LIMIT)
            or (replied.video and replied.video.file_name.endswith('.mp4')
                and replied.video.file_size <= _T_LIMIT)
            or (replied.document
                and replied.document.file_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.gif', '.mp4'))
                and replied.document.file_size <= _T_LIMIT)):
        await message.err("not supported!")
        return
    await message.edit("`processing...`")
    c_time = time.time()
    dl_loc = await userbot.download_media(
        message=message.reply_to_message,
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(
            "trying to download", userbot, message, c_time
        )
    )
    await message.edit("`uploading to telegraph...`")
    try:
        response = upload_file(dl_loc)
    except Exception as t_e:
        await message.err(t_e)
    else:
        await message.edit(f"**[Here Your Telegra.ph Link!](https://telegra.ph{response[0]})**")
    finally:
        os.remove(dl_loc)
