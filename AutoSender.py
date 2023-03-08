from datetime import time, date, datetime, timedelta
from time import sleep
from botVK import send_now
from variables import lesson_time
from funcs import get_log
import os

time_delta_5 = timedelta(minutes=5)
time_delta_1 = timedelta(minutes=1)

def group_autosend():
    def send(id):
        date_today = date.today()
        time_now = datetime.today()
        print("Now:", time_now.time())
        for tim in lesson_time:
            sleep_time = 120
            start_time = datetime.combine(date_today, time.fromisoformat(tim[:tim.find("-")]))
            final_time = datetime.combine(date_today, time.fromisoformat(tim[tim.find("-")+1:]))
            print('Time:', (start_time-time_delta_5).time(), "-", final_time.time())
            if start_time-time_delta_5 <= time_now <= start_time:
                send_now(id, "soon")
                print("Complete - soon", time_now)
                sleep_time = 5400
                return sleep_time
            elif final_time-time_delta_1 <= time_now <= final_time+time_delta_1:
                send_now(id, "next")
                print("Complete - next", time_now)
                return sleep_time
        print("Not that time")
        return sleep_time
            
    dir = os.listdir('./log_user')
    for ld in dir:
        id = int(ld[4:ld.find('.')])
        print("Autosend id =",id)
        group, rass = get_log(id)
        if rass == "да":
            sleep_time = send(id)
    sleep(sleep_time)

def main():
    while True:
        group_autosend()

if __name__ == "__main__":
    # send_now(id, "soon", time_now)
    main()
    
    