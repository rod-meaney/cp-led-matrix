'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import displayio
import os, time

class Animation(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, json_data, piType)
            
    def run(self):
        self.ShowImageBitmapLoaded(self.animations[self.current_animation_index])
        if self.current_animation_index == len(self.animations) - 1:
           self.current_animation_index = 0
        else:
           self.current_animation_index += 1
        time.sleep(self.animation_sleep)
        self.display.refresh(minimum_frames_per_second=0)
        
    def load(self, json_data):
        self.animation_sleep = 0.1
        self.current_animation_index = 0
        self.animations = []
        directory = json_data["directory"]
        contents = os.listdir(f'./animation/{directory}')
        for item in contents:
            bitmap = displayio.OnDiskBitmap(f'./animation/{directory}/{item}')
            self.animations.append(bitmap)
        
    @staticmethod
    def get_data():
        #Later
        animations = []
        contents = os.listdir('./animation')
        for item in contents:
            animations.append(item.replace('_', ' '))
        animations.sort()
        return {"animations":animations}
        
        
        
