'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import adafruit_display_text.label
import time, math
import displayio
import terminalio

class CountDown(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, json_data, piType)
            
    def run(self):
        reamining_time = self.end_time - time.monotonic()
        mins = math.floor(reamining_time/60)
        secs = math.floor(reamining_time%60)
        self.countdown.text = f'{mins}:{secs}'
        self.display.refresh(minimum_frames_per_second=0)
        
    def load(self, json_data):
        #Initialise
        self.countdown_heading = adafruit_display_text.label.Label(terminalio.FONT, text="mm:ss", x=0, y=10, color=0xFFFFFF)
        self.countdown_heading.color = self.get_color(json_data["color"])
        self.center_label(self.countdown_heading)
        
        self.countdown = adafruit_display_text.label.Label(terminalio.FONT, text="mm:ss", x=0, y=22, color=0xFFFFFF)
        self.countdown.color = self.get_color(json_data["color"])
        self.center_label(self.countdown)
        
        self.start_time = time.monotonic()
        self.countdown_mins = json_data["mins_to_countdown"]
        self.end_time = self.start_time + (self.countdown_mins*60)
        g = displayio.Group()
        g.append(self.countdown_heading)
        g.append(self.countdown)
        self.display.root_group = g

