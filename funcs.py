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
    r = data[day.title()]
    otvet = day.title() + f"\n"
    links = []
    if r["les_have"] == 0:
        otvet = otvet + f'\nВ этот день пар нет\n'
        return [otvet, links]
    for i in range(r["les_have"]):
        lin = None
        les_sm = None
        i = str(i+1)
        if r["les_" + i] != None:
            otvet += f"\n⏰ {r['tim_' + i]}\n✏️ {r['les_' + i]}\n👨‍🏫 {r['prep_' + i]}\n"
            try:
                otvet += f"Проходит в {r['aud_' + i]}\n"
            except:
                pass
            otvet += f"📅 {r['date_' + i]}\n"
            try:
                les_sm = r['les_sm_' + i]
                lin = r['lin_' + i]
                links += [[les_sm, lin]]
            except:
                pass
    
    if "special" in r:
        otvet += f'\n\nДополнение: {r["special"]}\n'
    otvet += f'\n{now.strftime("%A, %d. %B %Y %I:%M%p")}'
    return [otvet, links]

def get_now_rasp(id, mode="now", time_mode=None):
    group, rass = get_log(id)
    data = get_json_d(group)
    otvet = ""
    links = []
    wek = datetime.today().weekday()
    day = weekday_d[wek]
    date_today = date.today()
    time_delta = timedelta(minutes=5)
    time_delta_1 = timedelta(minutes=1)
    
    if time_mode:
        datetime_now = datetime.combine(date_today, time_mode)
    else:
        datetime_now = datetime.today()
    
    print(datetime_now)
    
    if wek == 6:
        otvet = "Сегодня нет пар!"
        return [otvet, links]

    for ir in range(data[day]["les_have"]):
        i = str(ir+1)
        tim = data[day]["tim_" + i]
        min_time = datetime.combine(date_today, time.fromisoformat(tim[:tim.find("-")]))
        max_time = datetime.combine(date_today, time.fromisoformat(tim[tim.find("-")+1:]))
        if min_time-time_delta <= datetime_now <= max_time+time_delta_1:
            if mode == "now":
                otvet = f"Сейчас идет:\n\n"
            elif mode == "soon":
                otvet = f"Скоро начнется:\n\n"
            elif mode == "next":
                otvet = f"Следущий занятие:\n\n"
            if mode == "next":
                if ir+1 < data[day]["les_have"]:
                    i = str(ir+2)
                else:
                    otvet = "На сегодня пары закончились!"
                    return [otvet, links]
            tim = data[day]["tim_" + i]
            
            otvet += f"✏️ Предмет: {data[day]['les_' + i]}\n"
            if mode == "soon" or mode == "next":
                otvet += f"⏰ Начало в {tim}\n"
            otvet += f"👨‍🏫 Преподаватель: {data[day]['prep_' + i]}\n"
            try:
                otvet += "Проходит в " + data[day]["aud_" + i] + f"\n"
            except:
                pass
            try:
                links = [[data[day]["les_sm_" + i], data[day]["lin_" + i]]]
            except:
                pass
            return [otvet, links]
    
    if mode == "now":
        otvet = f"Сейчас нет пар!"
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
