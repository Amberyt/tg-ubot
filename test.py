import os
import asyncio
from userbot import userbot


async def worker() -> None:
    chat_id = int(os.environ.get("CHAT_ID") or 0)
    await userbot.send_message(chat_id, 'testing_userbot')
    print('sleeping 3 sec...!')
    await asyncio.sleep(3)


async def main() -> None:
    print('starting client...!')
    await userbot.start()
    tasks = []
    print('adding tasks...!')
    for task in userbot._tasks:
        tasks.append(loop.create_task(task()))
    print('stating worker...!')
    await worker()
    print('closing tasks...!')
    for task in tasks:
        task.cancel()
    print('stopping client...!')
    await userbot.stop()

loop = asyncio.get_event_loop()
print('creating loop...!')
loop.run_until_complete(main())
print('closing loop...!')
loop.close()

print('userbot test has been finished!')
