'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import adafruit_display_text.label
from adafruit_display_shapes.rect import Rect
import time, math
import displayio
import terminalio

class Halloween(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        #time.sleep(0.005)
        if self.Hal_image_time:
            if self.Hal_Right:
                self.tile_grid.x += 1
                if self.tile_grid.x > self.display.width:
                    self.Hal_Right = False
            else:
                self.tile_grid.x -= 1
                if self.tile_grid.x < 0:
                    self.Hal_Right = True
                    if self.Hal_Image_cur_index == len(self.Hal_Images) - 1:
                        self.Hal_Image_cur_index = 0
                        self.Hal_image_time = False
                        self.Hal_Up = True
                    else:
                        self.Hal_Image_cur_index += 1
                    self.ShowImage(f'img/{self.Hal_Images[self.Hal_Image_cur_index]}.bmp')
            if self.Hal_Up:
                self.tile_grid.y += 1
                if self.tile_grid.y > 10:
                    self.Hal_Up = False
            else:
                self.tile_grid.y -= 1
                if self.tile_grid.y < 0:
                    self.Hal_Up = True
        else:
            new_line = adafruit_display_text.label.Label(terminalio.FONT, text="Happy Halloween!!", color=0xFFA500, x = 0, y = 16)
            self.center_label(new_line)
            g = displayio.Group()
            g.append(new_line)
            BORDER_THICKNESS = 2  # Adjust as needed
            self.border = Rect(x=0, y=0, width=self.display.width, height=self.display.height, outline=0xFFA500, stroke=BORDER_THICKNESS)        
            g.append(self.border)
            self.display.root_group = g
            for key in self.data["colors"]:
                self.border.outline = self.get_color(key)
                self.display.refresh(minimum_frames_per_second=0)
                time.sleep(0.5)
            count = 0
            while count < 8:
                for key in self.data["colors"]:
                    new_line.color = self.get_color(key)
                    self.display.refresh(minimum_frames_per_second=0)
                    time.sleep(0.1)
                count += 1
            self.Hal_image_time = True
            self.ShowImage(f'img/spider.bmp')
            
        self.display.refresh(minimum_frames_per_second=0)
        
    def load(self, json_data):
        self.Hal_image_time = False
        self.Hal_Up = True
        self.Hal_Right = True
        self.Hal_Images = ["spider", "ghost", "witch", "mask"]
        self.Hal_Image_cur_index = 0
        self.ShowImage(f'img/spider.bmp')

    def update(self, json_data):
        pass