import csv
import os

charset = set()
selectsuffix=("csv","json")

for dirpath, dirnames, filenames in os.walk("."):
    for f in filenames:
        #print(dirpath, dirnames, f)
        temppath = os.path.join(dirpath, f)
        if(f.endswith(selectsuffix)):
            print(temppath) 
            with open(temppath, mode = "r", encoding = "utf-8") as fi:
                tempBuf = fi.read()
                print("open:" ,temppath)
                for ch in tempBuf:
                    charset.add(ch)

charsetfile = open("charset.txt", mode="w", encoding="utf-8")
if charsetfile is not None:
    for ch in charset:
        charsetfile.write(ch)
charsetfile.close()
print("生成字符集完成")