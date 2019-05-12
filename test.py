import numpy as np
import random
import colorama
from colorama import Fore, Back, Style

colorama.init()

x = np.zeros((4,4), dtype=np.int)


x[0][0] = 32
x[1][3] = 2
x[3][2] = 4
x[1][2] = 8
x[3][3] = 1024
x[2][1] = 2000048

colors ={
    0: 47,
    2: 42,
    4: 42,
    8: 42,
    16: 41,
    32: 41,
    64: 41,
    128: 43,
    256: 43,
    512: 43,
    1024: 43,
    2048: 46
}

width = len(str(np.max(x)))
line = '_'*((width+1)*4 + 3)
print(len(line))
for row in x:
    print ("|".join(("\x1b[6;30;%sm %*s"+'\x1b[0m') % (str(colors.get(n,46)),width, str(n)) for n in row))
    print (line)
