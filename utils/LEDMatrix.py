'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
import adafruit_display_text.label
from adafruit_datetime import datetime, timedelta
import framebufferio
import displayio
import rgbmatrix
import board
import terminalio
import time
import json

class LEDMatrix(object):
    '''
    Nothing but the simplest base functions
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
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
        
        #Constants needed
        self.sleep = 0.05
        self.start_time = time.monotonic() #When the new display is started
        self.tz_offset = int(tzOffset)
        
        self.requests = requests
        self.ssl_requests = ssl_requests
        
        #Default time to show current matrix 0 = forever
        self.mins = 0
        if "mins" in json_data:
            self.mins = int(json_data["mins"])
        self.on = True

        #Set the data for any of the classes to use as necessary
        self.data = data

        #Set the start screen as blank
        self.BlankScreen()
        self.display.refresh(minimum_frames_per_second=0)
        self.load(json_data)
           
    def poll(self):
        if self.on:
            time.sleep(self.sleep) #This may become configurable
            if self.mins > 0:
                if (time.monotonic() - self.start_time) > self.mins*60:
                    self.BlankScreen()
                    self.on = False
                    
            #here we call out to specific class
            self.run()
        
    def center_label(self, label):
        label.x = (self.display.width // 2) - int(label.width // 2)

    def center_label_left_side(self, label):
        label.x = (self.display.width // 4) - int(label.width // 2)
        
    def center_label_right_side(self, label):
        label.x = (self.display.width // 4)*3 - int(label.width // 2)

    def get_color(self, color):
        if(color in self.data["colors"]):
            return bytes.fromhex(self.data["colors"][color])
        else:
            return bytes.fromhex(self.data["colors"]["Red"])
    
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
        ctime = (datetime.now() + timedelta(seconds=self.tz_offset)).timetuple()
        if seconds:
            label.text=f"{ctime.tm_hour:02}" + ':' + f"{ctime.tm_min:02}" + ':' + f"{ctime.tm_sec:02}"
        else:
            label.text=f"{ctime.tm_hour:02}" + ':' + f"{ctime.tm_min:02}"
        self.center_label(label)
        
    def text_label(self, text):
        line.x = line.x
        
    def BlankScreen(self):
        black_palette = displayio.Palette(1)
        black_palette[0] = 0x000000  # Black color (RGB565)    
        background_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        background_tilegrid = displayio.TileGrid(background_bitmap, pixel_shader=black_palette)
        g = displayio.Group()
        g.append(background_tilegrid)
        self.display.root_group = g
        self.display.refresh(minimum_frames_per_second=0)
        
    def ShowImage(self, img_file):
        bitmap = displayio.OnDiskBitmap(f'./{img_file}')
        self.ShowImageBitmapLoaded(bitmap)
        
    def ShowImageBitmapLoaded(self, bitmap):
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        group = displayio.Group()
        group.append(tile_grid)
        self.display.root_group = group
        self.display.refresh(minimum_frames_per_second=0)

class LEDMatrixBasic(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
    
    def load(self,json_data):
        self.label = adafruit_display_text.label.Label(terminalio.FONT, text=json_data["text"], color=self.get_color(json_data["color"]), x=0, y=12)
        g = displayio.Group()
        g.append(self.label)
        self.display.root_group = g
        
    def run(self):
        self.scroll_label(self.label)
        self.display.refresh(minimum_frames_per_second=0)
        
class LEDMatrixStop(LEDMatrix):
    '''
    standard starts with a blank screen, so nothing to do
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
    
    def load(self,json_data):
        pass
        
    def run(self):
        pass
    