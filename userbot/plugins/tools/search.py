from userbot import userbot, Message


@userbot.on_cmd("s", about={
    'header': "search commands in USERBOT",
    'examples': "{tr}s wel"})
async def search(message: Message):
    cmd = message.input_str
    if not cmd:
        await message.err(text="Enter any keyword to search in commands")
        return
    found = [i for i in sorted(list(userbot.manager.enabled_commands)) if cmd in i]
    out_str = '    '.join(found)
    if found:
        out = f"**--I found ({len(found)}) commands for-- : `{cmd}`**\n\n`{out_str}`"
    else:
        out = f"__command not found for__ : `{cmd}`"
    await message.edit(text=out, del_in=0)
