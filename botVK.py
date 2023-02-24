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

    
def sender(id, text, keyboard=None):
    post = {id_name : id, 'message' : text, 'random_id' : 0}
    if keyboard!=None:
        post['keyboard']=keyboard.get_keyboard()
    bot.method('messages.send', post)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:
                text = event.text.lower()
                id = event.chat_id
                print('chat text: ' + text + f' id: {id}')
                slovo = text
                keyboard = None
                otvet = ""
                keyb_e = False
                if slovo == "начать":
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
                            Приветствую! \nНапиши мне номер своей группы и я буду показывать вам расписание для нее! \n\nТакже дайте разрешение на автоматическую рассылку, что бы автоматически получать сообщения о начале пары.\n\nОбразец сообщения: Группа: xxx-xxx Авторассылка: да\n\nМожно присылать по отдельности, однако прошу писать сообщение строго по образцу!
                            """
                
                if "/понедельник" in slovo:
                    
                    try:
                        otvet, keyb = funcs.rasp(id, "Понедельник")
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
                        otvet = f"Возникла ошибка: "+str(ex)
                    
                if "/вторник" in slovo:
                    keyboard = VkKeyboard(inline=True)
                    try:
                        otvet, keyb = funcs.rasp(id, "Вторник")
                        if keyb:
                            k = len(keyb)
                            keyb_e = True
                            for sn, l in keyb:
                                k = k - 1
                                keyboard.add_openlink_button(f'{sn}',f'{l}')
                                if k: keyboard.add_line()
                                print(sn)

                    except Exception as ex:
                        otvet = f"Возникла ошибка: "+str(ex)
                        
                if "/среда"  in slovo:
                    keyboard = VkKeyboard(inline=True)
                    
                    try:
                        otvet, keyb = funcs.rasp(id, "Среда")
                        if keyb:
                            keyb_e = True
                            k = len(keyb)
                            for sn, l in keyb:
                                k = k - 1
                                keyboard.add_openlink_button(f'{sn}',f'{l}')
                                if k: keyboard.add_line()
                                print(sn)

                    except Exception as ex:
                        otvet = f"Возникла ошибка: "+str(ex)       
                        
                if "/четверг"  in slovo:
                    keyboard = VkKeyboard(inline=True)
                    try:
                        otvet, keyb = funcs.rasp(id, "Четверг")
                        if keyb:
                            k = len(keyb)
                            keyb_e = True
                            for sn, l in keyb:
                                k = k - 1
                                keyboard.add_openlink_button(f'{sn}',f'{l}')
                                if k: keyboard.add_line()
                                print(sn)

                    except Exception as ex:
                        otvet = f"Возникла ошибка: "+str(ex)
                
                if "/пятница" in slovo:
                    keyboard = VkKeyboard(inline=True)
                    try:
                        otvet, keyb = funcs.rasp(id, "Пятница")
                        if keyb:
                            k = len(keyb)
                            keyb_e = True
                            for sn, l in keyb:
                                k = k - 1
                                keyboard.add_openlink_button(f'{sn}',f'{l}')
                                if k: keyboard.add_line()
                                print(sn)

                    except Exception as ex:
                        otvet = f"Возникла ошибка: "+str(ex)  
                        
                if "/суббота" in slovo:
                    keyboard = VkKeyboard(inline=True)
                    try:
                        otvet, keyb = funcs.rasp(id, "Суббота")
                        if keyb:
                            k = len(keyb)
                            keyb_e = True
                            for sn, l in keyb:
                                k = k - 1
                                keyboard.add_openlink_button(f'{sn}',f'{l}')
                                if k: keyboard.add_line()
                                print(sn)

                    except Exception as ex:
                        otvet = f"Возникла ошибка: " + str(ex)
                
                if "/цитата_волка" in slovo:
                    with open('Citati.txt', 'r', encoding='utf-8') as f:
                        citati = f.read().split(f"\n")
                        f.close()
                    r = random.randint(0, len(citati)-1)
                    otvet = f"Цитата №{r+1}\n"+citati[r]
                
                if "/сейчас" in slovo:
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
                
                if "группа:" in slovo or "авторассылка:" in slovo:
                    try:
                        otvet = funcs.make_log(text, id)
                    except Exception as ex:
                        otvet = f"Возникла ошибка: " + str(ex)
                
                if "/обновить_расписание" in slovo:
                    try:
                        sender(id, "Подождите пожалуйста.", None)
                        funcs.update(id)
                        otvet = "Расписание обновлено!"
                    except Exception as ex:
                        otvet = f"Возникла ошибка: " + str(ex)
                
                if "/stop" in slovo:
                    sender(id, "Goodbye!", None)
                    exit()
                
                if otvet:
                    if keyb_e:
                        sender(id, otvet, keyboard)
                    else:
                        sender(id, otvet, None)
                        


