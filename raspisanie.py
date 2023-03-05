from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from variables import months, weekdays
import time
import datetime
import json
import os.path
import os

def find_group(gr):
    url = "https://rasp.dmami.ru/"
    file_name = f"./rasp_html/rasp_for_{gr}.txt"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
        options.headless = True
        driver = webdriver.Chrome(service=Service("./cromedriver/chromedriver.exe"), options=options)
        driver.get(url=url)
        time.sleep(2)
        groups = driver.find_element(by=By.CLASS_NAME, value="groups")
        groups.clear()
        groups.send_keys(gr)
        time.sleep(2)
        gr_button = driver.find_element(by=By.ID, value=gr)
        gr_button.click()
        time.sleep(2)
        week = driver.find_element(by=By.CLASS_NAME, value="schedule-week")

        with open(file_name, "w", encoding="utf8") as file:
            file.write(week.get_attribute("innerHTML"))
            file.close()
    except Exception as ex:
        print(str(ex))
        pass
    finally:
        driver.close()
        driver.quit()
    print(f"Create {file_name}")
    return file_name

def get_all_rasp(group):
    fn_html = f"./rasp_html/rasp_for_{group}.txt"
    fn_json = f"./rasp_json/rasp_for_{group}.json"
    if os.path.exists(fn_html):
        with open(fn_html, "r", encoding="utf8") as fp:
            src = fp.read()
            soup = bs(src, "lxml")

        days = soup.find_all("div", class_="schedule-day")
        less_all = {}
        l = 0
        for day in days:
            day_title = day.find("div", class_="schedule-day__title").text.strip()
            less_all.update({day_title : {}})
            pairs = day.find("div", class_="pairs")
            pair = pairs.find_all("div", class_="pair")
            less_all[day_title].update({"id":l})
            l += 1
            k = 0
            for pai in pair:
                lessons = pai.find("div", class_="lessons")
                lesson = lessons.find_all("div", class_="schedule-lesson")
                tim = pai.find("div", class_="time").text.strip()
                if len(tim)<11: tim = "0" + tim

                for lesso in lesson:
                    lesson_cl = lesso.get_attribute_list("class")
                    if not 'schedule-day_old' in lesson_cl:
                        
                        les = lesso.find("div", class_="bold").text.strip()
                        les_sm = les
                        lin = lesso.find("div", class_="schedule-auditory").find("a")
                        aud = lesso.find("div", class_="schedule-auditory").text.strip()
                        prep = lesso.find("div", class_="teacher").text.strip()
                        date = lesso.find("div", class_="schedule-dates").text.strip()
                        date_fp = date.split(" ")
                        today_date = datetime.date.today()
                        min_date = datetime.date(today_date.year, months[date_fp[1]], int(date_fp[0]))
                        max_date = datetime.date(today_date.year, months[date_fp[4]], int(date_fp[3]))
                        print(day_title, ":", min_date, "|", max_date, "|", today_date)
                        
                        if min_date <= today_date <= max_date:
                            k = k + 1
                            if len(les_sm)>39:
                                les_sm = les_sm[:les.find("(")].strip()
                                if len(les_sm)>39:
                                    les_sm = les_sm[:39].strip()
                            less_all[day_title].update(
                                {
                                    f"tim_{k}": tim,
                                    f"les_{k}" : les,
                                    f"les_sm_{k}" : les_sm,
                                    f"prep_{k}" : prep,
                                }
                            )

                            if lin == None:
                                less_all[day_title].update({f"aud_{k}": aud})
                            else:
                                less_all[day_title].update(
                                    {
                                        f"aud_{k}": aud,
                                        f"lin_{k}": lin.get("href")
                                    }
                                )
                            less_all[day_title].update({f"date_{k}":date})
                        
            less_all[day_title].update({"les_have":k})

        data = json.dumps(less_all, indent=2, ensure_ascii=False)

        with open(fn_json, "w", encoding="utf8") as file:
            file.write(data)
        print(f"Create {fn_json}")
        return fn_json
    else:
        find_group(group)
        get_all_rasp(group)

    