from datetime import datetime
import botVK

if __name__ == "__main__":
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
