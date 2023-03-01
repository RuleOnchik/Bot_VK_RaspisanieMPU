from datetime import datetime
from threading import Thread
import botVK

if __name__ == "__main__":
    thread_bot = Thread(target=botVK.main)
    print('Activate bot at', datetime.now().strftime("%I:%M%p"))
    continue_bot = True
    while continue_bot:
        try:
            thread_bot.start()
            thread_bot.join()
            print('Deactivate bot at', datetime.now().strftime("%I:%M%p"))
            if input(f"Reactivate bot? Yes/No\n") in ["Yes", "yes", "Y", "y", "1"]:
                raise Exception
            else:
                print("Goodbye!")
                continue_bot = False
        except:
            print('Reactivate bot at', datetime.now().strftime("%I:%M%p"))
