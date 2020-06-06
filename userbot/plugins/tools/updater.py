import asyncio

from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError

from userbot import userbot, Message, Config

LOG = userbot.getLogger(__name__)
CHANNEL = userbot.getCLogger(__name__)

UPSTREAM_REMOTE = 'upstream'


@userbot.on_cmd("update", about={
    'header': "Check Updates or Update Userbot",
    'flags': {
        '-pull': "pull updates",
        '-push': "push updates to heroku",
        '-master': "select master branch",
        '-beta': "select beta branch",
        '-dev': "select dev branch"},
    'usage': "{tr}update : check updates from default branch\n"
             "{tr}update -[branch_name] : check updates from any branch\n"
             "add -pull if you want to pull updates\n"
             "add -push if you want to push updates to heroku",
    'examples': "{tr}update -beta -pull -push"}, del_pre=True)
async def check_update(message: Message):
    """check or do updates"""
    await message.edit("`Checking for updates, please wait....`")
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
    if UPSTREAM_REMOTE in repo.remotes:
        ups_rem = repo.remote(UPSTREAM_REMOTE)
    else:
        ups_rem = repo.create_remote(UPSTREAM_REMOTE, Config.UPSTREAM_REPO)
    try:
        ups_rem.fetch()
    except GitCommandError as error:
        await message.err(error, del_in=5)
        return
    for ref in ups_rem.refs:
        branch = str(ref).split('/')[-1]
        if branch not in repo.branches:
            repo.create_head(branch, ref)
    flags = list(message.flags)
    pull_from_repo = False
    push_to_heroku = False
    branch = "master"
    if "pull" in flags:
        pull_from_repo = True
        flags.remove("pull")
    if "push" in flags:
        push_to_heroku = True
        flags.remove("push")
    if len(flags) == 1:
        branch = flags[0]
    if branch not in repo.branches:
        await message.err(f'invalid branch name : {branch}')
        return
    out = ''
    try:
        for i in repo.iter_commits(f'HEAD..{UPSTREAM_REMOTE}/{branch}'):
            out += (f"🔨 **#{i.count()}** : "
                    f"[{i.summary}]({Config.UPSTREAM_REPO.rstrip('/')}/commit/{i}) "
                    f"👷 __{i.committer}__\n\n")
    except GitCommandError as error:
        await message.err(error, del_in=5)
        return
    if out:
        if pull_from_repo:
            await message.edit(f'`New update found for [{branch}], Now pulling...`')
            await asyncio.sleep(1)
            repo.git.reset('--hard', 'FETCH_HEAD')
            await CHANNEL.log(f"**UPDATED Userbot from [{branch}]:\n\n📄 CHANGELOG 📄**\n\n{out}")
        elif not push_to_heroku:
            changelog_str = f'**New UPDATE available for [{branch}]:\n\n📄 CHANGELOG 📄**\n\n'
            await message.edit_or_send_as_file(changelog_str + out, disable_web_page_preview=True)
            return
    elif not push_to_heroku:
        await message.edit(f'**Userbot is up-to-date with [{branch}]**', del_in=5)
        return
    if not push_to_heroku:
        await message.edit(
            '**Userbot Successfully Updated!**\n'
            '`Now restarting... Wait for a while!`', del_in=3)
        asyncio.get_event_loop().create_task(userbot.restart(update_req=True))
        return
    if not Config.HEROKU_GIT_URL:
        await message.err("please set heroku things...")
        return
    await message.edit(
        f'`Now pushing updates from [{branch}] to heroku...\n'
        'this will take upto 3 min`\n\n'
        '* **Restart** me after about 3 min using `.restart -h`\n\n'
        '* After restarted successfully, check updates again :)')
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(Config.HEROKU_GIT_URL)
    else:
        remote = repo.create_remote("heroku", Config.HEROKU_GIT_URL)
    remote.push(refspec=f'{branch}:master', force=True)
    await message.edit(f"**HEROKU APP : {Config.HEROKU_APP.name} is up-to-date with [{branch}]**")
