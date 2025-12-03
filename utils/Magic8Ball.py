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
import random

class Magic8Ball(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        #change it up - cannot dynamically change width of rect
        if self.iterations == 0:
            if self.answered == False:
                self.BlankScreen()
                self.label = adafruit_display_text.label.Label(terminalio.FONT, text=self.answers[self.answer_index], color=self.get_color("Blue"), x=0, y=12)
                self.scroll = False
                if self.label.width > self.display.width:
                    self.label.x = self.display.width
                    self.scroll = True
                else:
                    #center
                    self.center_label(self.label)
                g = displayio.Group()
                g.append(self.label)
                self.display.root_group = g
                self.display.refresh(minimum_frames_per_second=0)
                self.answered = True
            else:
                if self.scroll == True:
                    self.scroll_label(self.label)
                    self.display.refresh(minimum_frames_per_second=0)
                
            
        elif (time.monotonic() - self.last_moved) > (self.next_move):
            self.border_y += 1
            if self.border_y == 16:
                self.border_y = 0
                border = Rect(x=0,
                              y=self.border_y,
                              width=self.display.width,
                              height=self.display.height,
                              outline=self.wait_colour,
                              stroke=self.border_thickness)
                self.g.append(border)
                self.display.root_group = self.g
            else:
                border = Rect(x=self.border_y,
                              y=self.border_y,
                              width=self.display.width - (self.border_y * 2),
                              height=self.display.height - (self.border_y * 2),
                              outline=self.wait_colour,
                              stroke=self.border_thickness)
                self.g.append(border)
            
            #self.border.outline = self.get_color(self.colour_keys[self.colour_index])
            self.next_move = self.next_move - 0.1
            self.iterations -= 1
            self.last_moved = time.monotonic()
            self.display.refresh(minimum_frames_per_second=0)
    
    def load(self, json_data):
        #Initialise
        self.colour_index = 0
        self.colour_keys = []
        self.border_thickness = 1
        self.border_y = 0
        self.last_moved = time.monotonic()
        self.next_move = 1 #time until next move
        self.iterations = 10 #when it will stop
        self.answered = False
        self.answers = ["It is certain","Reply hazy, try again","Don't count on it","It is decidedly so","Ask again later","My reply is no","Without a doubt","Better not tell you now","My sources say no","Yes definitely","Cannot predict now","Outlook not so good","You may rely on it","Concentrate and ask again","Very doubtful","As I see it, yes","Most likely","Outlook good","Yes","Signs point to yes"]
        self.answer_index = random.randint(1, len(self.answers)) - 1
        self.g = displayio.Group()
        for key in self.data["colors"]:
            self.colour_keys.append(key)
        
        self.wait_colour = self.get_color(self.colour_keys[random.randint(1, len(self.colour_keys)) - 1])
        #Add a border
        border = Rect(x=0,
                      y=self.border_y,
                      width=self.display.width,
                      height=self.display.height,
                      outline=self.wait_colour,
                      stroke=self.border_thickness)
        self.g.append(border)
            
        self.display.root_group = self.g
        self.display.refresh(minimum_frames_per_second=0)

    def update(self, json_data):
        #Only reason it is here is the pause button has been hit
        pass