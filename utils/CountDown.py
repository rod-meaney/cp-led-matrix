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

class CountDown(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        if self.still_going:
            remaining_time = self.end_time - time.monotonic()
            hours = math.floor(remaining_time/3600)
            remaining_mins = remaining_time - hours*3600
            mins = math.floor(remaining_mins/60)
            secs = math.floor(remaining_mins%60)
            self.countdown.text = f'{hours:02}:{mins:02}:{secs:02}'
            self.display.refresh(minimum_frames_per_second=0)
            if hours == mins == secs == 0:
                self.still_going = False
        else:
            for key in self.data["colors"]:
                self.border.outline = self.get_color(key)
                self.display.refresh(minimum_frames_per_second=0)
                time.sleep(0.5)
            
        
    def load(self, json_data):
        #Initialise
        self.still_going = True
        self.countdown_heading = adafruit_display_text.label.Label(terminalio.FONT, text="hh:mm:ss", x=0, y=10, color=0xFFFFFF)
        self.countdown_heading.color = self.get_color(json_data["color"])
        self.center_label(self.countdown_heading)
        
        self.countdown = adafruit_display_text.label.Label(terminalio.FONT, text="hh:mm:ss", x=0, y=22, color=0xFFFFFF)
        self.countdown.color = self.get_color(json_data["color"])
        self.center_label(self.countdown)
        
        self.start_time = time.monotonic()
        self.countdown_mins = json_data["mins_to_countdown"]
        self.end_time = self.start_time + (self.countdown_mins*60)
        g = displayio.Group()
        g.append(self.countdown_heading)
        g.append(self.countdown)
        
        #Add a border
        BORDER_THICKNESS = 2  # Adjust as needed
        self.border = Rect(x=0, y=0, width=self.display.width, height=self.display.height, outline=self.countdown.color, stroke=BORDER_THICKNESS)        
        g.append(self.border)
            
        self.display.root_group = g

