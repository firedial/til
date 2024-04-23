import json
from paifu import Paifu

f = open('paifu/mahjongsoul_paifu_220508-33d67351-5ec4-4799-9a26-a78c1da05b4f.txt')
p = Paifu(json.load(f))
f.close()

print(p.debug())

