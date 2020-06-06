from userbot import userbot, Message


@userbot.on_cmd("json", about={
    'header': "message object to json",
    'usage': "reply {tr}json to any message"})
async def jsonify(message: Message):
    the_real_message = str(message.reply_to_message) if message.reply_to_message \
        else str(message)
    await message.edit_or_send_as_file(text=the_real_message,
                                       filename="json.txt",
                                       caption="Too Large")
