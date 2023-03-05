import datetime

s = "01 Сен - 20 Фев"
date = s.split(" ")
print(date)
months ={"Янв": 1, "Фев": 2, "Мар": 3, "Апр": 4, "Май": 5, "Июн": 6, "Июл": 7, "Авг": 8, "Сен": 9, "Окт": 10, "Ноя": 11, "Дек": 12}
t = datetime.date.today()
d = datetime.date(2022, months[date[1]], int(date[0]))
if t<d:
    print(d)
else:
    print('no')
    print(d)

ts = "09:00-13:50"
tst = datetime.time.fromisoformat(ts[:ts.find("-")])
print(tst)
wek = datetime.datetime.today().weekday()
print(wek)

time_now = datetime.datetime.today().time()
j_time = datetime.time(14,30)
if j_time < time_now:
    print(j_time)
else:
    print(time_now)
    
# if 5<6<3:
    # print("qwerty")
# else:
    # print("poiuygtfbn")