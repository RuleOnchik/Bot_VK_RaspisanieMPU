from raspisanie import get_all_rasp
import json
from datetime import datetime, date, time, timedelta
from variables import weekdays, weekday_d
import os

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
        return f"Возникла ошибка: {str(ex)}"

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
    if "special" in r:
        otvet = otvet + f'\n\nДополнение: {r["special"]}\n'
    keyboard = links
    otvet = otvet + f'\n{now.strftime("%A, %d. %B %Y %I:%M%p")}'
    return [otvet, keyboard]

def get_now_rasp(id, mode="now", time_mode=None):
    group, rass = get_log(id)
    data = get_json_d(group)
    wek = datetime.today().weekday()
    time_n = datetime.today()
    time_now = datetime.fromisoformat("1991-01-01T"+f"{time_n.hour if len(str(time_n.hour))==2 else '0'+str(time_n.hour)}")
    if mode == "now":
        otvet = f"Сейчас идет:\n"
    elif mode == "soon":
        otvet = f"Скоро начнется:\n"
    elif mode == "next":
        otvet = f"Следущий занятие:\n"
    time_delta = timedelta(minutes=5)
    
    # wek = 1
    # time_n = "12:18"
    # time_now = datetime.fromisoformat("1991-01-01T"+time_n)
    
    link = ""
    links = []
    d = weekday_d[wek]
    print(d)
    if wek == 6:
        otvet = "Сегодня нет пар!"
        return [otvet, link]
    if data[d]["les_have"]:
        for i in range(data[d]["les_have"]):
            i = str(i+1)
            tim = data[d]["tim_" + i]
            print("Время: ",tim)
            min_time = datetime.fromisoformat("1991-01-01T"+tim[:tim.find("-")])
            max_time = datetime.fromisoformat("1991-01-01T"+tim[tim.find("-")+1:])
            if min_time-time_delta <= time_now <= max_time:
                if (int(i)+1 != data[d]["les_have"]):
                    if mode == "next":
                        i = str(int(i)+1)
                        tim = data[d]["tim_" + i]
                elif min_time-time_delta >= time_now:
                    otvet = ""
                    return [otvet, links]
                elif time_now >= max_time:
                    otvet = "На сегодня пары закончились"
                    return [otvet, links]
                if mode == "soon" or mode == "next":
                    otvet += "⏰ Начало в " + tim + f"\n" 
                otvet += "✏️ Предмет: " + data[d]["les_" + i] + f"\n"
                otvet += "👨‍🏫 Преподаватель: " + data[d]["prep_" + i] + f"\n"
                try:
                    otvet += "Проходит в " + data[d]["aud_" + i] + f"\n"
                except:
                    pass
                try:
                    link = data[d]["lin_" + i]
                    sn = data[d]["les_sm_" + i]
                    links = [[sn, link]]
                except:
                    pass
                return [otvet, links]

    otvet = "Сейчас нет пар!"
    return [otvet, links]

def add_special(id, mess):
    group, rass = get_log(id)
    with open(f'./rasp_json/rasp_for_{group}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if ":" in mess:
        text = mess[mess.find(":")+1:].strip()
        mode = mess[:mess.find(":")].split("/")
    else:
        mode = mess.split("/")
    if mode[0] == "записать":
        data[mode[1].capitalize()].update({ "special": text})
        otvet = 'Запись сохранена!'
    elif mode[0] == "добавить":
        if "special" in data[mode[1].capitalize()]:
            data[mode[1].capitalize()].update({ "special": data[mode[1].capitalize()]["special"] + f'\n' + text})
        else:
            data[mode[1].capitalize()].update({ "special": text})
        otvet = 'Запись добавлена!'
    elif mode[0] == "удалить":
        if "special" in data[mode[1].capitalize()]:
            data[mode[1].capitalize()].pop("special")
        otvet = 'Дополнительная запись удалена!'
    
    data_d = json.dumps(data, indent=2, ensure_ascii=False)
    
    with open(f'./rasp_json/rasp_for_{group}.json', "w", encoding="utf8") as file:
        file.write(data_d)
    
    return otvet

def update(id):
    group, rass = get_log(id)

    fn_html = f"./rasp_html/rasp_for_{group}.txt"
    fn_json = f"./rasp_json/rasp_for_{group}.json"
    if os.path.isfile(fn_html): 
        os.remove(fn_html) 
        print("html removed") 
    else: 
        print("HTML file doesn't exists!")
    
    if os.path.isfile(fn_json): 
        special = []
        with open(f'./rasp_json/rasp_for_{group}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for day in weekdays:
            if "special" in data[day[1:].capitalize()]:
                special.append([day[1:].capitalize(), data[day[1:].capitalize()]["special"]])
        os.remove(fn_json) 
        print("json removed") 
    else: 
        print("Json file doesn't exists!")
    
    get_all_rasp(group)
    
    if special:
        with open(f'./rasp_json/rasp_for_{group}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for day, text in special:
            data[day]["special"] = text
        data_d = json.dumps(data, indent=2, ensure_ascii=False)
        with open(f'./rasp_json/rasp_for_{group}.json', "w", encoding="utf8") as file:
            file.write(data_d)

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
