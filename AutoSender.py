import funcs
import os
import botVK
import funcs
import asyncio

def main():
    files = os.listdir(path="./log_user/")
    print(files)
    for file in files:
        with open("./log_user/" + file, encoding="utf8") as read:
            r = read.read()
            id = int(file[file.find("_")+1:file.find(".")])
            print("id =", id)
            group, autsend = funcs.get_log(id)
            if id == 2:
                botVK.sender(id, "Привет, твоя группа: " + group)

async def test():
    print("привет")

asyncio.run(test())