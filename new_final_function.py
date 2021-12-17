# original lib
import cv2 
import time
import imutils
import numpy as np
import argparse
import matplotlib.pyplot as plt

# my lib
from extract_contours import ExtractContour
from id_finder import GridMaker
from angle import Angle
from Samarth_CNN.shape_identifier import ShapeIdentifier

shape_identifier = ShapeIdentifier()

class BotFinder:
    def __init__(self):#,f_no):

        self.bot_ID_all = []
        self.bot_angle = []
        self.Bot = {}
        self.AC_orientation = []
        self.rotated_img = 0

        
        #region show extracted bot
        # for i in range(len(bot_img)):
        #    cv2.imshow(f'{i}', bot_img[i])
        # cv2.waitKey()
        #endregion
    
    def give_frame(self,img):

        self.img = img
        #extract 4 bot images and store it in 'bot_img'
        #'self.bot_location' contains its position 
        ext = ExtractContour(self.img)
        bot_img,self.bot_location = ext.ret()
        
        #initialize shape detector
        aligned_images = []
        s = time.time()
        
        for i in range(len(bot_img)):
            bot_img[i] = cv2.resize(bot_img[i], (int( bot_img[i].shape[1]*4) , int(bot_img[i].shape[0]*4)))            
   
            # find angle of alignment of bot with +ve x-aixs 'degree'
            # stores the rotated image to 'self.rotated_img'
            Agl = Angle(bot_img[i])
            degree,self.rotated_img = Agl.ret()
            self.AC_orientation.append(degree)

            # give exracted contours of shape
            gd = GridMaker(self.rotated_img)
            shape_imgs= gd.ShapeImages()
            self.curr_bot_id = ''
            for j in range(4):
                try: 
                    if shape_imgs[j] == None:
                        # print('empty')
                        self.curr_bot_id+=str(0)
                        continue
                except:pass
                cv2.imwrite('useless_file.png', shape_imgs[j])
                in_img = plt.imread('useless_file.png')
                shape = shape_identifier.predict(in_img)
                if shape == 0:
                    # print('circle')
                    self.curr_bot_id+=str(2)
                elif shape == 1:
                    # print('triangle')
                    self.curr_bot_id+=str(1)

            self.bot_ID_all.append(self.curr_bot_id)    
            self.Bot[self.curr_bot_id] = self.bot_location[i]
        e = time.time()
        print(s-e)
    def ret(self):    
        count = 0
        for i in self.Bot.keys():
            temp = self.Bot[i]
            self.Bot[i] = [temp[0],temp[1], self.AC_orientation[count]]
            count = count + 1
        return self.Bot

if __name__ == '__main__':
    feed = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{63}.jpg')
    BF = BotFinder()
    for i in range(5):
       BF.give_frame(feed)
       bot = BF.ret()
