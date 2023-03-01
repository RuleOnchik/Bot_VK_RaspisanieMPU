import funcs
import os

files = os.listdir(path="./log_user/")
print(files)
for file in files:
    with open("./log_user/"+file, encoding="utf8") as read:
        r = read.read()
        id = file[file.find("_")+1:file.find(".")]
        print("id =", id)

