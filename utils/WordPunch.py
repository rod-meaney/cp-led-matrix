'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import adafruit_display_text.label
import displayio
import terminalio

class WordPunch(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        self.wordpunch_label.x  = self.wordpunch_label.x -1
        label_width = self.wordpunch_label.bounding_box[2]
        if self.wordpunch_label.x < -label_width:
            #change the word
            if self.wordpunch_index == len(self.wordpunch) - 1:
                self.wordpunch_index = 0
            else:
                self.wordpunch_index += 1
            self.wordpunch_label.text = self.wordpunch[self.wordpunch_index]
            # put the word to the right
            self.wordpunch_label.x = self.width
        self.display.refresh(minimum_frames_per_second=0)
        
    def load(self, json_data):
        #Initialise
        self.wordpunch_label = adafruit_display_text.label.Label(terminalio.FONT, text="", color=0xFFFFFF)
        self.wordpunch_label.color = self.get_color(json_data["color"])
        if json_data["big"] == True:
            self.wordpunch_label.scale = 2 
        self.wordpunch = json_data["sentence"].split()
        self.sleep = float(json_data["sleep"])
        
        self.wordpunch_index = 0
        self.wordpunch_label.text = self.wordpunch[0]
        self.wordpunch_label.x = self.width
        
        self.wordpunch_label.anchor_point = (0.5, 0.5)
        self.wordpunch_label.anchored_position = (self.display.width // 2, self.display.height // 2)
        g = displayio.Group()
        g.append(self.wordpunch_label)
        self.display.root_group = g
