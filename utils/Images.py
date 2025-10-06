'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import os

class Images(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        pass
        
    def load(self, json_data):
        file = json_data["file"]
        self.ShowImage(f'img/{file}.bmp')
        
    @staticmethod
    def get_data():
        #Later
        animations = []
        contents = os.listdir('./img')
        for item in contents:
            animations.append(item.replace('_', ' '))
        animations.sort()
        return {"images":animations}
        
        
        
