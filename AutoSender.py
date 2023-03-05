import datetime
from funcs import get_now_rasp
from botVK import sender, send_now
import os

def send_rasp(mode="soon"):
    id = 2
    otvet, keyboard = send_now(id, mode)
    sender(id, otvet, keyboard=keyboard)

if __name__ == "__main__":
    send_rasp("next")
    