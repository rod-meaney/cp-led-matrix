'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
import os
from utils.config import PMConfig
import adafruit_display_text.label
from adafruit_datetime import datetime, timedelta
import adafruit_imageload
import framebufferio
import displayio
import rgbmatrix
import board
import terminalio
import time, math
import json

class PMMatrix(object):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, piType="pico"):
        self.initialise = True
        displayio.release_displays()
        #Set up the board
        if piType == "pico":
            self.matrix = rgbmatrix.RGBMatrix(
                width=64, height=32, bit_depth=2,
                rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
                addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
                clock_pin=board.GP10, latch_pin=board.GP11, output_enable_pin=board.GP12)
            #Special things to do with pico
            
        else:
            #Zero with Adafruit HAT
            self.matrix = rgbmatrix.RGBMatrix(
                width=64, height=32, bit_depth=2,
                rgb_pins=[board.GP5, board.GP13, board.GP6, board.GP12, board.GP16, board.GP23],
                addr_pins=[board.GP22, board.GP26, board.GP27, board.GP20],
                clock_pin=board.GP17, latch_pin=board.GP21, output_enable_pin=board.GP4)
        
        #Create the display
        self.display = framebufferio.FramebufferDisplay(self.matrix, auto_refresh=False)
        self.width = self.display.width #making it more specific
        self.labels = []
        
        #Constants needed
        self.sleep = 0.05
        self.animation_sleep = 0.1
        self.tz_offset = int(tzOffset)
        
        self.requests = requests
        self.ssl_requests = ssl_requests
        self.colors = {"Red":0xff0000, "Orange":0xFFA500, "Yellow":0xFFFF00, "Green":0x00FF00, "Blue":0x0000FF, "Indigo":0x4B0082, "Violet":0x7F00FF, "White":0xFFFFFF}
        with open('./data/cities.json', "r") as file:
            self.cities = json.load(file)    
        
        #Default time to show current matrix 0 = forever
        self.mins = 0
        self.on = False
        
        #Set the start screen as blank
        self.BlankScreen()
        self.display.refresh(minimum_frames_per_second=0)
    
    def NewMatrix(self, json):
        self.initialise = True
        self.labels = []
        self.on = True
        self.mins = int(json["mins"])
        self.start_time = time.monotonic() #When the new display is started
        self.last_tram_check = time.monotonic() #Need this so we only poll every 20 sec
        self.last_weather_check = time.monotonic() #Need this so we only poll every 300 sec
        self.temperature = 0
        self.temperature_missed = ''
        self.current_animation_index = 0
        self.animations = []
        self.wordpunch = []
        self.wordpunch_label = adafruit_display_text.label.Label(terminalio.FONT, text="", color=0xFFFFFF)
        self.wordpunch_index = 0
        self.tram_fails = 0 #if it gets to three we may want to throw error - create error framework (red screen and writing file)
        if json["name"] == "ThreeLines":
            self.ThreeLines(json)
        elif json["name"] == "TwoLines":
            self.ThreeLines(json, True)
        elif json["name"] == "CenteredText":
            self.CenteredText(json["distext"],json["color"])
        elif json["name"] == "Animation":
            self.LoadAnimation(json["directory"])
        elif json["name"] == "WordPunch":
            self.LoadWordPunch(json["sentence"], json["color"], json["sleep"])
            
    def poll(self):
        if self.on:
            time.sleep(self.sleep) #This may become configurable
            if self.mins > 0:
                if (time.monotonic() - self.start_time) > self.mins*60:
                    self.BlankScreen()
                    self.display.refresh(minimum_frames_per_second=0)
                    self.labels = []
                    self.animations = []
                    self.wordpunch = []
                    self.on = False
                
            #Check for run out of time and set to blank and clear labels
            for label in self.labels:
                if label["type"] == "scroll":
                    self.scroll_label(label["label"])
                elif label["type"] == "reverse_scroll":
                    self.reverse_scroll_label(label["label"])
                elif label["type"] == "clock":
                    self.clock_label(label["label"],label["data"]["seconds"])
                elif label["type"] == "tram":
                    self.tram_label(label["label"], label["data"]["stopNo"], label["data"]["routeNo"])
                elif label["type"] == "weather":
                    self.weather_label(label["label"], label["data"]["city"])
                self.display.refresh(minimum_frames_per_second=0)
            self.initialise = False
            
            # Need to re-code, img display not coming though here, so doing refresh for this separately - messy, FIX
            if len(self.animations) > 0:
                self.Animation()
                
            if len(self.wordpunch) > 0:
                self.WordPunch()
                self.display.refresh(minimum_frames_per_second=0)

    def center_label(self, label):
        label.x = (self.display.width // 2) - int(label.width // 2)

    def get_color(self, color):
        if(color in self.colors):
            return self.colors[color]
        else:
            return self.colors["Red"]
    
    def scroll_label(self, label):
        label.x  = label.x -1
        label_width = label.bounding_box[2]
        if label.x < -label_width:
            label.x = self.width 

    def reverse_scroll_label(self, label):
        label.x  = label.x + 1
        line_width = label.bounding_box[2]
        if label.x >= self.width:
            label.x = -line_width
            
    def clock_label(self, label, seconds):
        ctime = (datetime.now() + timedelta(hours=self.tz_offset)).timetuple()
        if seconds:
            label.text=f"{ctime.tm_hour:02}" + ':' + f"{ctime.tm_min:02}" + ':' + f"{ctime.tm_sec:02}"
        else:
            label.text=f"{ctime.tm_hour:02}" + ':' + f"{ctime.tm_min:02}"
        self.center_label(label)
        
    def text_label(self, text):
        line.x = line.x
        
    def tram_label(self, label, stopNo, routeNo):
        check_every = 20
        TramUrl=f"http://tramtracker.com.au/Controllers/GetNextPredictionsForStop.ashx?stopNo={stopNo}&routeNo={routeNo}&isLowFloor=false"
        
        if ((math.ceil(time.monotonic() - self.last_tram_check) % check_every)== 0) or self.initialise:
            self.last_tram_check = time.monotonic()
            response = self.requests.get(TramUrl)
            data = json.loads(response.text)
            next_trams = []
            next_tram_min = 1000 # just a large number which willbe greater than any next tram time
            for tram in data['responseObject']:
                dateStr = tram['PredictedArrivalDateTime']
                tram_epoch = dateStr[dateStr.index('(')+1:16]
                minute_diff = str((int((int(tram_epoch) - int(time.time()))/60)))
                next_trams.append(minute_diff)
                #setting up for colour
                if (int(minute_diff) < next_tram_min):
                    next_tram_min = int(minute_diff)
            
            #Set colour
            if next_tram_min < 4:
                label.color = self.get_color("Red")
            elif next_tram_min < 6:
                label.color = self.get_color("Orange")
            else:
                label.color = self.get_color("Green")

            label.text = ",".join(next_trams)
            self.center_label(label)
            
    def weather_label(self, label, city):
        check_every = 300 #5 minutes
        latitude = self.cities[city]['latitude']
        longitude = self.cities[city]['longitude']
        abbrev = self.cities[city]['abbrev']
        weatherurl =f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,cloud_cover,rain,precipitation,wind_speed_10m,showers,apparent_temperature'
        if ((math.ceil(time.monotonic() - self.last_weather_check) % check_every)== 0) or self.initialise:
            self.last_weather_check = time.monotonic()
            try:
                response = self.ssl_requests.get(weatherurl)
                data = json.loads(response.text)
                self.temperature = str(data['current']['temperature_2m'])
                self.temperature_missed = ''
            except Exception as e:
                self.temperature_missed = '*'
            label.text = f'{abbrev}:{self.temperature}{self.temperature_missed}'
            self.center_label(label)
            
    def Animation(self):
        self.ShowImageBitmapLoaded(self.animations[self.current_animation_index])
        if self.current_animation_index == len(self.animations) - 1:
           self.current_animation_index = 0
        else:
           self.current_animation_index += 1
        time.sleep(self.animation_sleep)
        
    def LoadAnimation(self, directory):
        contents = os.listdir(f'./animation/{directory}')
        for item in contents:
            bitmap = displayio.OnDiskBitmap(f'./animation/{directory}/{item}')
            self.animations.append(bitmap)
            
    def WordPunch(self):
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
            
        
    def LoadWordPunch(self, sentence, color, sleep):
        self.wordpunch = sentence.split()
        self.sleep = sleep
        self.wordpunch_label.text = self.wordpunch[0]
        self.wordpunch_label.x = self.width
        self.wordpunch_label.color = self.get_color(color)
        self.wordpunch_label.anchor_point = (0.5, 0.5)
        self.wordpunch_label.anchored_position = (self.display.width // 2, self.display.height // 2)
        g = displayio.Group()
        g.append(self.wordpunch_label)
        self.display.root_group = g

    def BlankScreen(self):
        black_palette = displayio.Palette(1)
        black_palette[0] = 0x000000  # Black color (RGB565)    
        background_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        background_tilegrid = displayio.TileGrid(background_bitmap, pixel_shader=black_palette)
        g = displayio.Group()
        g.append(background_tilegrid)
        self.labels = [] #Clear labels
        self.animations = [] #Clear anaimations
        self.wordpunch = [] #Clear words
        self.display.root_group = g
        self.display.refresh(minimum_frames_per_second=0)

    def CenteredText(self, distext, color):
        text_label = adafruit_display_text.label.Label(terminalio.FONT, text=distext, color=0xFFFFFF)
        # Set anchor point to the center of the text
        text_label.anchor_point = (0.5, 0.5)
        # Set anchored position to the center of the display
        text_label.anchored_position = (self.display.width // 2, self.display.height // 2)
        #set the color
        text_label.color = self.get_color(color)
        # Create a display group and add the label
        g = displayio.Group()
        self.labels = []
        g.append(text_label)
        self.labels.append({"type":"scroll","label":text_label})
        self.display.root_group = g

    def ThreeLines(self, config):
        g = displayio.Group()
        num_lines = len(config["lines"])
        if num_lines == 1:
            ys = [16]
        elif num_lines == 2:
            ys = [10,22]
        else:
            ys = [6,16,26]
        
        i=0
        for line in config["lines"]:
            new_line = adafruit_display_text.label.Label(terminalio.FONT, text="loading", color=0xFFFFFF, x = 0, y = ys[i])
            if "color" in line:
                new_line.color = self.get_color(line["color"])
            if "text" in line:
                new_line.text = line["text"]
                self.center_label(new_line)
            g.append(new_line)
            self.labels.append({"type":line["type"],"label":new_line, "data":line["data"]})
            i+=1
        
        self.display.root_group = g

    def ShowImage(self, img_file):
        bitmap = displayio.OnDiskBitmap(f'./{img_file}')
        self.ShowImageBitmapLoaded(bitmap)
    
    def ShowImageBitmapLoaded(self, bitmap):
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        group = displayio.Group()
        group.append(tile_grid)
        self.display.root_group = group
        self.display.refresh(minimum_frames_per_second=0)

    def ShowSpriteMap(self, img_file):
        # Load the sprite sheet (bitmap)
        sprite_sheet, palette = adafruit_imageload.load("./img/cp_sprite_sheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
        
        sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16)
        # Create a Group to hold the sprite
        group = displayio.Group(scale=1)

        # Add the sprite to the Group
        group.append(sprite)

        # Add the Group to the Display
        self.display.root_group = group

        # Set sprite location
        group.x = 10
        group.y = 10

        # Loop through each sprite in the sprite sheet
        source_index = 0
        while True:
            sprite[0] = source_index % 6
            source_index += 1
            self.display.refresh(minimum_frames_per_second=0)
            time.sleep(2)
        