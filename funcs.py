from raspisanie import get_all_rasp, update_rasp
import json
from datetime import datetime, date, time, timedelta

def make_log(text, id):
    print('make_log:',text)
    group = ""
    rass = ""

    try:
        with open(f"./log_user/log_{id}.txt", "r", encoding="utf8") as file:
            dd = file.read()
        print(dd)
        dd = dd.split(" ")
        if "Группа:" in dd:
            group = dd[dd.index("Группа:")+1]
        if "Авторассылка:" in dd:
            rass = dd[dd.index("Авторассылка:")+1]
    except:
        pass
        
    if rass == "":
        rass = "нет"
    if group == "":
        group = "нет"
        
    try:
        text = text.lower().split(" ")
        print(text)
        if "группа:" in text:
            group = text[text.index("группа:")+1]
        if "авторассылка:" in text:
            rass = text[text.index("авторассылка:")+1]
        with open(f"./log_user/log_{id}.txt", "w", encoding="utf8") as file:
            write_text = f"Группа: {group} Авторассылка: {rass}"
            print("Новая запись:", write_text)
            file.write(write_text)
        return "Данные успешно обновлены"
    except Except as ex:
        return f"Возникла ошибка: {ex}"

def get_json_d(group):
    try:
        with open(f'./rasp_json/rasp_for_{group}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except:
        get_all_rasp(group)
        return get_json_d(group)

def get_log(id):
    try:
        with open(f"./log_user/log_{id}.txt", "r", encoding="utf8") as file:
            dd = file.read()
        dd = dd.split(" ")
        group = ""
        rass = ""
        if "Группа:" in dd:
            try:
                group = dd[1]
            except:
                group = ""
        if "Авторассылка:" in dd:
            try:
                rass = dd[3]
            except:
                rass = ""
        if group is not None and rass is not None:
            return (group, rass)
    except:
        raise Exception("Вы не задали логи")

def rasp(id, day):
    group, rass = get_log(id)

    data = get_json_d(group)
    now = datetime.now()
    name_r = day.title()
    r = data[name_r]
    otvet = name_r
    tim = None
    les = None
    les_sm = None
    aud = None
    lin = None
    prep = None
    les_date = None
    i = [1, 2, 3, 4, 5, 6, 7]
    links = []
    if r["les_have"]:
        for i in i:
            aud = None
            lin = None
            try:
                i = str(i)
                if r["les_" + i] != None:
                    tim = "⏰" + r["tim_" + i]
                    les = "✏️" + r["les_" + i]
                    les_sm = r["les_sm_" + i]
                    les_date = "📅" + r["date_" + i]
                    try:
                        aud = r["aud_" + i]
                    except:
                        pass
                    try:
                        lin = r["lin_" + i]
                    except:
                        pass
                    prep = "👨‍🏫" + r["prep_" + i]
                    otvet = otvet + f'\n\n{tim}'
                    otvet = otvet + f'\n{les}'
                    otvet = otvet + f'\n{prep}'
                    if aud != None:
                        otvet = otvet + f'\nПроходит в {aud}'
                    if lin != None:
                        links += [[les_sm, lin]]
                    otvet = otvet + f'\n{les_date}'
            except:
                pass
    elif r["les_have"] == 0:
        otvet = otvet + f'\n\nВ этот день пар нет\n'
    keyboard = links
    otvet = otvet + f'\n{now.strftime("%A, %d. %B %Y %I:%M%p")}'
    return [otvet, keyboard]

def get_now_rasp(id):
    group, rass = get_log(id)
    data = get_json_d(group)
    wek = datetime.today().weekday()
    i = [1, 2, 3, 4, 5, 6, 7]
    otvet = ""
    link = ""
    links = []
    for d in data:
        if data[d]["id"] == wek:
            if data[d]["les_have"]:
                for i in range(data[d]["les_have"]):
                    try:
                        i = str(i+1)
                        tim = data[d]["tim_" + i]
                        print(tim)
                        if len(tim[:tim.find("-")])<5:
                            tim = "0" + tim
                        min_time = time.fromisoformat(tim[:tim.find("-")])
                        if len(tim[tim.find("-")+1:])<5:
                            tim = tim[:tim.find("-")] + "0" + tim[tim.find("-")+1:]
                        max_time = time.fromisoformat(tim[tim.find("-")+1:])
                        time_now = datetime.today().time()
                        if time_now >= min_time and time_now <= max_time:
                            otvet += "✏️ Сейчас идет: " + data[d]["les_" + i] + f"\n"
                            otvet += "👨‍🏫 Преподаватель: " + data[d]["prep_" + i] + f"\n"
                            try:
                                otvet += "Проходит в: " + data[d]["aud_" + i] + f"\n"
                            except:
                                pass
                            try:
                                link = data[d]["lin_" + i]
                                sn = data[d]["les_sm_" + i]
                                links = [[sn, link]]
                            except:
                                pass
                            return [otvet, links]
                    
                    except Exception as ex:
                        raise Exception(ex)

    otvet = "Сейчас нет пар"
    return [otvet, link]
    
def update(id):
    group, rass = get_log(id)
    update_rasp(group)

def test(id):
    try:
        print("1")
        with open(f"./log_user/log_{id}.txt", "r", encoding="utf8") as file:
            dd = file.read()
        print(dd)
        dd = dd.split(" ")
        if "Группа:" in dd:
            print(dd[1])
    except:
        with open(f"./log_user/log_{id}.txt", "w", encoding="utf8") as file:
            file.write("Группа: 201-341")
        test(id)
