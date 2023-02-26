import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import time
import subprocess
import datetime
import funcs
import random

tok = '53a987c023bf8f643b9504614a8241fc1269160637a7e1e836a544483383344de8f9390e66982d77b8bde'

bot = vk_api.VkApi(token = tok)
longpoll = VkLongPoll(bot)
id_name = 'chat_id'

weekdays = ['/понедельник', '/вторник', '/среда', '/четверг', '/пятница', '/суббота']

def main():
    print('Star main')
    
    start_bot()

def sender(id, text, keyboard=None):
    # nonlocal bot, id_name
    post = {id_name : id, 'message' : text, 'random_id' : 0}
    if keyboard!=None:
        post['keyboard']=keyboard.get_keyboard()
    bot.method('messages.send', post)

def start_bot():
    # nonlocal bot, longpoll, weekdays
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.from_chat:
                    text = event.text.lower()
                    id = event.chat_id
                    print('chat text: ' + text + f' id: {id}')
                    keyboard = None
                    otvet = ""
                    keyb_e = False
                    if text == "начать" or text == "привет":
                        keyb_e = True
                        keyboard = VkKeyboard()
                        keyboard.add_button('/Понедельник', VkKeyboardColor.PRIMARY)
                        keyboard.add_button('/Вторник', VkKeyboardColor.PRIMARY)
                        keyboard.add_line()
                        keyboard.add_button('/Среда', VkKeyboardColor.PRIMARY)
                        keyboard.add_button('/Четверг', VkKeyboardColor.PRIMARY)
                        keyboard.add_line()
                        keyboard.add_button('/Пятница', VkKeyboardColor.PRIMARY)
                        keyboard.add_button('/Суббота', VkKeyboardColor.PRIMARY)
                        keyboard.add_line()
                        keyboard.add_button('/Цитата_волка', VkKeyboardColor.NEGATIVE)
                        keyboard.add_button('/Сейчас', VkKeyboardColor.POSITIVE)
                        keyboard.add_line()
                        keyboard.add_button('/Обновить_расписание', VkKeyboardColor.PRIMARY)
                        otvet = f"""
                                Приветствую! \nНапиши мне номер своей группы и я буду показывать вам расписание для нее! \n\nТакже дайте разрешение на автоматическую рассылку, что бы автоматически получать сообщения о начале пары.(в разработке)\n\nОбразец сообщения: Группа: xxx-xxx Авторассылка: да/нет\n\nМожно присылать по отдельности, однако прошу писать сообщение строго по образцу!\n\nОсновные функции: \nПросмотр расписания на определенный день недели\nПросмотр предмета, который идет сейчас\nВывод цитаты волка(АУФ)
                                """
                    ####################
                    for day in weekdays:
                        if day in text:
                            try:
                                otvet, keyb = funcs.rasp(id, day[1:].capitalize())
                                if keyb:
                                    keyboard = VkKeyboard(inline=True)
                                    k = len(keyb)
                                    keyb_e = True
                                    for sn, l in keyb:
                                        k = k - 1
                                        keyboard.add_openlink_button(f'{sn}',f'{l}')
                                        if k: keyboard.add_line()
                                break
                            except Exception as ex:
                                otvet = f"Возникла ошибка: "+str(ex)
                                break
                    ############################
                    if "/цитата_волка" in text:
                        with open('Citati.txt', 'r', encoding='utf-8') as f:
                            citati = f.read().split(f"\n")
                            f.close()
                        r = random.randint(0, len(citati)-1)
                        otvet = f"Цитата №{r+1}\n"+citati[r]
                    ######################
                    if "/сейчас" in text:
                        try:
                            otvet, keyb = funcs.get_now_rasp(id)
                            if keyb:
                                keyboard = VkKeyboard(inline=True)
                                k = len(keyb)
                                keyb_e = True
                                for sn, l in keyb:
                                    k = k - 1
                                    keyboard.add_openlink_button(f'{sn}',f'{l}')
                                    if k: keyboard.add_line()
                                    print(sn)
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
                    ##################################################
                    if "группа:" in text or "авторассылка:" in text:
                        try:
                            otvet = funcs.make_log(text, id)
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
                    ###################################
                    if "/обновить_расписание" in text:
                        try:
                            sender(id, "Подождите пожалуйста.")
                            funcs.update(id)
                            otvet = "Расписание обновлено!"
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
                    ####################
                    if "/stop" in text:
                        sender(id, "Goodbye!")
                        break
                    #########
                    if otvet:
                        sender(id, otvet, keyboard)
                            
if __name__ == "__main__":
    main()