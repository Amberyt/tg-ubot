from userbot import userbot, Message, Config, versions


@userbot.on_cmd("repo", about={'header': "get repo link and details"})
async def see_repo(message: Message):
    """see repo"""
    output = f"""
**Hey**, __I am using__ 🔥 **Userbot** 🔥
× **userbot version** : `{versions.__version__}`
× **repo** : [tg_ubot]({Config.UPSTREAM_REPO})
"""
    await message.edit(output)
