'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import os, math, time

class Images(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        if self.img_slide_show:
            if ((math.ceil(time.monotonic() - self.last_change) % self.check_every) == 0):
                if self.last_index == len(self.rotating_images) - 1:
                    self.last_index = 0
                else:
                    self.last_index += 1
                self.ShowImage(f'img/{self.rotating_images[self.last_index]}')
                self.last_change = time.monotonic()
                time.sleep(self.check_every)
        
        
    def load(self, json_data):
        self.check_every = 10
        self.img_slide_show = False
        file = json_data["file"]
        self.ShowImage(f'img/{file}.bmp')
        if json_data["slideShow"]:
            self.img_slide_show = True
            self.rotating_images = self.get_data()
            self.last_change = time.monotonic()
            self.last_index = 0
        
    @staticmethod
    def get_data():
        #Later
        animations = []
        contents = os.listdir('./img')
        for item in contents:
            animations.append(item)
        animations.sort()
        return animations
        
        
        
