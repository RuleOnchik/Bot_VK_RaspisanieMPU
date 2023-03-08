import json
from datetime import time, datetime, timedelta
import os

print(os.listdir('./log_user/'))
ld = os.listdir('./log_user/')
print(ld[0][4:ld[0].find('.')])

a = time(9,58,32)
b = time(16,58,33)
s = "09:24-12:45"
st = datetime.now().time()
print(int("03"))
print(st)
print(a)
print(b)
time_delta = timedelta(minutes=5)
if a > st+time_delta:
    print("a > s")
else:
    print("b > s")















# s = "01 Сен - 20 Фев"
# date = s.split(" ")
# print(date)
# months ={"Янв": 1, "Фев": 2, "Мар": 3, "Апр": 4, "Май": 5, "Июн": 6, "Июл": 7, "Авг": 8, "Сен": 9, "Окт": 10, "Ноя": 11, "Дек": 12}
# t = datetime.date.today()
# d = datetime.date(2022, months[date[1]], int(date[0]))
# if t<d:
    # print(d)
# else:
    # print('no')
    # print(d)

# ts = "09:00-13:50"
# tst = datetime.time.fromisoformat(ts[:ts.find("-")])
# print(tst)
# wek = datetime.datetime.today().weekday()
# print(wek)

# time_now = datetime.datetime.today().time()
# j_time = datetime.time(14,30)
# if j_time < time_now:
    # print(j_time)
# else:
    # print(time_now)
    
# if 5<6<3:
    # print("qwerty")
# else:
    # print("poiuygtfbn")
    
    
# def add_sp(group, mess="записать/понедельник: текст"):
    # with open(f'./rasp_json/rasp_for_{group}.json', 'r', encoding='utf-8') as file:
        # data = json.load(file)
    
    # text = mess[mess.find(":")+1:].strip()
    # mode = mess[:mess.find(":")].split("/")
    
    # if mode[0] == "записать":
        # data[mode[1].capitalize()].update({ "special": text})
    # elif mode[0] == "добавить":
        # if "special" in data[mode[1].capitalize()]:
            # data[mode[1].capitalize()].update({ "special": data[mode[1].capitalize()]["special"] + f'\n' + text})
        # else:
            # data[mode[1].capitalize()].update({ "special": text})
    
    # data_d = json.dumps(data, indent=2, ensure_ascii=False)
    
    # with open(f'./rasp_json/rasp_for_{group}.json', "w", encoding="utf8") as file:
        # file.write(data_d)


# add_sp("201-363", "добавить/четверг: ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ!")