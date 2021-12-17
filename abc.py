import cv2
import numpy as np
from contour_finder import C_T_iden_fn
import imutils
import time


for i in range(1000,3000,1):
    path = f'C:/Users/OHM/Desktop/pytthon/bot_BW/{i}.png'
    temp = cv2.imread(path)
    # cv2.imshow('winname', temp)
    print(i)
    resize = cv2.resize(temp, (100,100))
    cv2.imwrite(path, resize)