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

class Score(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        self.display.refresh(minimum_frames_per_second=0)
        
    def load(self, json_data):
        #Initialise
        self.comp_heading = adafruit_display_text.label.Label(terminalio.FONT, text=json_data["competition"], x=0, y=6, color=0xFFFFFF)
        self.comp_heading.color = self.get_color(json_data["color"])
        self.center_label(self.comp_heading)
        
        self.Team1_name = adafruit_display_text.label.Label(terminalio.FONT, text=json_data["team1"], x=0, y=16, color=0xFFFFFF)
        self.Team1_name.color = self.get_color(json_data["team1_color"])
        self.center_label_left_side(self.Team1_name)

        self.team1_total = int(json_data["team1_score"])
        self.Team1_score = adafruit_display_text.label.Label(terminalio.FONT, text=json_data["team1_score"], x=0, y=26, color=0xFFFFFF)
        self.Team1_score.color = self.get_color(json_data["team1_color"])
        self.center_label_left_side(self.Team1_score)

        self.Team2_name = adafruit_display_text.label.Label(terminalio.FONT, text=json_data["team2"], x=0, y=16, color=0xFFFFFF)
        self.Team2_name.color = self.get_color(json_data["team2_color"])
        self.center_label_right_side(self.Team2_name)

        self.team2_total = int(json_data["team2_score"])
        self.Team2_score = adafruit_display_text.label.Label(terminalio.FONT, text=json_data["team2_score"], x=0, y=26, color=0xFFFFFF)
        self.Team2_score.color = self.get_color(json_data["team2_color"])
        self.center_label_right_side(self.Team2_score)

        g = displayio.Group()
        g.append(self.comp_heading)
        g.append(self.Team1_name)
        g.append(self.Team1_score)
        g.append(self.Team2_name)
        g.append(self.Team2_score)        
            
        self.display.root_group = g
        
    def update(self, json_data):
        if (json_data["team"])=="team1":
            self.team1_total = self.team1_total + int(json_data["update"])
            self.Team1_score.text = str(self.team1_total)
        else:
            self.team2_total = self.team2_total + int(json_data["update"])
            self.Team2_score.text = str(self.team2_total)
