#https://www.youtube.com/watch?v=p4YirERTVF0
import random
import math


#Universal repulsion constant
PHI = 10
#Universal zero constant
TAU = 20
#max/min
PI = (TAU-PHI)/2


def func(x1,x2,y1,y2,m:float,color):
    #m is between 0 and 1
    r = math.sqrt((x2-x1)**2+(y2-y1)**2)
    slope = m*(1/(PI-PHI))
    if r <= PHI:
        return -1
    elif PHI < r < PI:
        return slope*(r-PHI)
    elif PI < r < TAU:
        return -slope*(r-PHI)
    else:
        return 0


def fx(item):
    return item[0]


def fy(item):
    return item[1]


class Particles:

    def __init__(self,color=0):
        pass

    def update(self):
        pass
