from datetime import datetime
from threading import Thread
import botVK
import asyncio

async def autosend():
    pass

if __name__ == "__main__":
    thread_bot = Thread(target=botVK.main)
    print('Activate bot at', datetime.now().strftime("%I:%M%p"))
    continue_bot = True
    while continue_bot:
        try:
            botVK.main()
            print('Deactivate bot at', datetime.now().strftime("%I:%M%p"))
            continue_bot = False
        except:
            print('Reactivate bot at', datetime.now().strftime("%I:%M%p"))
            # continue_bot = False
