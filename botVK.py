import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import time
import subprocess
import datetime
import funcs
from variables import token, id_name, weekdays
import random

bot = vk_api.VkApi(token = token)
longpoll = VkLongPoll(bot)

def sender(id, text, bot = bot, keyboard=None):
    # nonlocal bot, id_name
    post = {id_name : id, 'message' : text, 'random_id' : 0}
    if keyboard!=None:
        post['keyboard']=keyboard.get_keyboard()
    bot.method('messages.send', post)

def send_now(id, mode="now"):
    otvet, keyb = funcs.get_now_rasp(id, mode)
    keyboard = None
    if keyb:
        keyboard = VkKeyboard(inline=True)
        k = len(keyb)
        keyb_e = True
        for sn, l in keyb:
            k = k - 1
            keyboard.add_openlink_button(f'{sn}',f'{l}')
            if k: keyboard.add_line()
    return [otvet, keyboard]

def start_bot(bot = bot):
    # nonlocal bot, longpoll, weekdays
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.from_chat:
                    text = event.text.lower()
                    id = event.chat_id
                    print(f'chat <{id}> text: ' + text)
                    keyboard = None
                    otvet = ""
                    keyb_e = False
                    ########################################
                    if text == "начать, бот" or text == "привет, бот":
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
                        # keyboard.add_line()
                        # keyboard.add_button('/Обновить_расписание', VkKeyboardColor.PRIMARY)
                        otvet = f"""
                                Приветствую! \nНапиши мне номер своей группы и я буду показывать вам расписание для нее! \n\nТакже дайте разрешение на автоматическую рассылку, что бы автоматически получать сообщения о начале пары.(в разработке)\n\nОбразец сообщения: Группа: xxx-xxx Авторассылка: да/нет\n\nМожно присылать по отдельности, однако прошу писать сообщение строго по образцу!\n\nОсновные функции: \n• Просмотр расписания на определенный день недели\n• Просмотр предмета, который идет сейчас\n• Добавить определенному дню недели дополнительную запись\nㅤПример: Записать/Понедельник: Текст\nㅤЕсть 3 режима: Записать, Добавить или Удалить. В первом случае предыдущие записи стираются, во втором - дописывается в конец, в третьем - запись удаляется\n• Вывод цитаты волка(АУФ)
                                """
                    ################################################
                    if "группа:" in text or "авторассылка:" in text:
                        try:
                            otvet = funcs.make_log(text, id)
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
                    ####################################################################
                    if "записать/" in text or "добавить/" in text or "удалить/" in text:
                        try:
                            otvet = funcs.add_special(id, text)
                            sender(id, otvet)
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
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
                    ###########################
                    if "/цитата_волка" in text:
                        with open('Citati.txt', 'r', encoding='utf-8') as f:
                            citati = f.read().split(f"\n")
                            f.close()
                        r = random.randint(0, len(citati)-1)
                        otvet = f"Цитата №{r+1}\n"+citati[r]
                    #####################
                    if "/сейчас" in text:
                        try:
                            otvet, keyboard = send_now(id)
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
                    ##################################
                    if "/обновить_расписание" in text:
                        try:
                            sender(id, "Подождите пожалуйста.")
                            funcs.update(id)
                            otvet = "Расписание обновлено!"
                        except Exception as ex:
                            otvet = f"Возникла ошибка: " + str(ex)
                    ###################
                    if "/stop" in text:
                        sender(id, "Goodbye!", bot)
                        break
                    #########
                    if otvet:
                        sender(id, otvet, bot, keyboard)

def main():
    print('Star main')
    
    start_bot()

if __name__ == "__main__":
    main()
