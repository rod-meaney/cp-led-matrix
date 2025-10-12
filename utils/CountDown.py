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
            if self.pause == False:
                #Only update if we are not paused
                self.remaining_time = self.end_time - time.monotonic()
                hours = math.floor(self.remaining_time/3600)
                remaining_mins = self.remaining_time - hours*3600
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
        self.pause = False
        self.countdown_heading = adafruit_display_text.label.Label(terminalio.FONT, text="hh:mm:ss", x=0, y=10, color=0xFFFFFF)
        self.countdown_heading.color = self.get_color(json_data["color"])
        self.center_label(self.countdown_heading)
        
        self.countdown = adafruit_display_text.label.Label(terminalio.FONT, text="hh:mm:ss", x=0, y=22, color=0xFFFFFF)
        self.countdown.color = self.get_color(json_data["color"])
        self.center_label(self.countdown)
        
        self.countdown_mins = json_data["mins_to_countdown"]
        self.end_time = time.monotonic() + (self.countdown_mins*60)
        self.remaining_time = self.end_time - time.monotonic()
        g = displayio.Group()
        g.append(self.countdown_heading)
        g.append(self.countdown)
        
        #Add a border
        BORDER_THICKNESS = 2  # Adjust as needed
        self.border = Rect(x=0, y=0, width=self.display.width, height=self.display.height, outline=self.countdown.color, stroke=BORDER_THICKNESS)        
        g.append(self.border)
            
        self.display.root_group = g

    def update(self, json_data):
        #Only reason it is here is the pause button has been hit
        if self.pause == False:
            self.pause = True
            self.countdown_heading.text = "PAUSED"
            self.center_label(self.countdown_heading)
            self.display.refresh(minimum_frames_per_second=0) #we pause on this until pause is clicked again
        else:
            self.end_time = time.monotonic() + self.remaining_time
            self.countdown_heading.text = "hh:mm:ss"
            self.center_label(self.countdown_heading)
            self.pause = False