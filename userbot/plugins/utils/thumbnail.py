import os
import time
from datetime import datetime
from userbot import userbot, Config, Message
from userbot.utils import progress

THUMB_PATH = Config.DOWN_PATH + "thumb_image.jpg"
CHANNEL = userbot.getCLogger(__name__)


@userbot.on_cmd('sthumb', about={
    'header': "Save thumbnail",
    'usage': "{tr}sthumb [reply to any photo]"})
async def save_thumb_nail(message: Message):
    await message.edit("processing ...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        start_t = datetime.now()
        c_time = time.time()
        if os.path.exists(THUMB_PATH):
            os.remove(THUMB_PATH)
        await userbot.download_media(message=replied,
                                    file_name=THUMB_PATH,
                                    progress=progress,
                                    progress_args=(
                                        "trying to download", userbot, message, c_time))
        end_t = datetime.now()
        m_s = (end_t - start_t).seconds
        await message.edit(f"thumbnail saved in {m_s} seconds.", del_in=3)
    else:
        await message.edit("Reply to a photo to save custom thumbnail", del_in=3)


@userbot.on_cmd('dthumb', about={'header': "Delete thumbnail"})
async def clear_thumb_nail(message: Message):
    await message.edit("`processing ...`")
    if os.path.exists(THUMB_PATH):
        os.remove(THUMB_PATH)
        await message.edit("✅ Custom thumbnail deleted succesfully.", del_in=3)
    elif os.path.exists('resources/tg-ubot.png'):
        os.remove('resources/tg-ubot.png')
        await message.edit("✅ Default thumbnail deleted succesfully.", del_in=3)
    else:
        await message.delete()


@userbot.on_cmd('vthumb', about={'header': "View thumbnail"})
async def get_thumb_nail(message: Message):
    await message.edit("processing ...")
    if os.path.exists(THUMB_PATH):
        msg = await userbot.send_document(chat_id=message.chat.id,
                                         document=THUMB_PATH,
                                         disable_notification=True,
                                         reply_to_message_id=message.message_id)
        await CHANNEL.fwd_msg(msg)
        await message.delete()
    else:
        await message.err("Custom Thumbnail Not Found!")
