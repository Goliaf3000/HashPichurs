import hashlib
import os

os.chdir("C:\\Users\\Андрей\\Downloads\\тест")
for e in os.listdir(path="."):
    print(e, hashlib.md5(open(e, 'rb').read()).hexdigest())
