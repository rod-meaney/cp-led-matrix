'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.LEDMatrix import LEDMatrix
import adafruit_display_text.label
from adafruit_bitmap_font import bitmap_font
import displayio
import terminalio
import time, math, json

class ThreeLines(LEDMatrix):
    '''
    Helper functions for the project
    '''

    def __init__(self, tzOffset, requests, ssl_requests, data, json_data, piType="pico"):
        super().__init__(tzOffset, requests, ssl_requests, data, json_data, piType)
            
    def run(self):
        for label in self.labels:
            if label["type"] == "scroll":
                self.scroll_label(label["label"])
            elif label["type"] == "reverse_scroll":
                self.reverse_scroll_label(label["label"])
            elif label["type"] == "clock":
                self.clock_label(label["label"],label["data"]["seconds"])
            elif label["type"] == "tram":
                self.tram_label(label)
            elif label["type"] == "weather":
                self.weather_label(label)
            elif label["type"] == "catfacts":
                self.cat_facts(label)
        self.initialise = False
        self.display.refresh(minimum_frames_per_second=0)
    
    def load(self, json_data):
        #Initialise
        self.initialise = True
        self.labels = []
        self.last_weather_check = time.monotonic() #Need this so we only poll every 300 sec
        self.temperature = 0
        self.temperature_missed = ''

        g = displayio.Group()
        num_lines = len(json_data["lines"])
        if num_lines == 1:
            ys = [16]
        elif num_lines == 2:
            ys = [10,22]
        else:
            ys = [6,16,26]
        
        i=0
        #font_path = "/fonts/font.pcf"
        #small_font = bitmap_font.load_font(font_path)
        for line in json_data["lines"]:
            new_line = adafruit_display_text.label.Label(terminalio.FONT, text="loading", color=0xFFFFFF, x = 0, y = ys[i])
            #new_line = adafruit_display_text.label.Label(small_font, text="loading", color=0xFFFFFF, x = 0, y = ys[i])
            if "color" in line:
                new_line.color = self.get_color(line["color"])
            if "text" in line:
                new_line.text = line["text"]
                self.center_label(new_line)
                
            g.append(new_line)
            self.labels.append({"type":line["type"],"label":new_line, "data":line["data"], "clock":time.monotonic()}) #clock added on if we need to keep track of time intervanls - i.e. calling external API's
            i+=1
        
        self.display.root_group = g
    
    @staticmethod
    def load_from_file(selected_file):
        filename = f'./saved/{selected_file}.json'
        with open(filename, "r") as file:
            data = json.load(file)
        return data
        
    def tram_label(self, row):
        label = row["label"]
        stopNo = row["data"]["stopNo"]
        routeNo = row["data"]["routeNo"]
        last_tram_check = row["clock"]
        showRoute = False
        try:
            showRoute = row["data"]["showRoute"]
        except Exception as e:
            # Making it backwards compatiable with earlier versions
            pass
        
        check_every = 20
        TramUrl=f"http://tramtracker.com.au/Controllers/GetNextPredictionsForStop.ashx?stopNo={stopNo}&routeNo={routeNo}&isLowFloor=false"
        
        if ((math.ceil(time.monotonic() - last_tram_check) % check_every)== 0) or self.initialise:
            try:
                row["clock"] = time.monotonic()
                time.sleep(self.sleep) #recommended to pause before sending requests from pico
                response = self.requests.get(TramUrl, timeout=2)
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
                if showRoute:
                    label.text = f'{routeNo}:{label.text}'
            except Exception as e:
                #Something failed - add a dot to make people aware
                label.text = label.text + '.'

            if label.width < self.width:
                self.center_label(label)
            
    def weather_label(self, row):
        #NOTE - this seems to chew up sockets and resources when it fails - have removed from front end selection
        label = row["label"]
        city = row["data"]["city"]
        check_every = 300 #5 minutes
        latitude = self.data["cities"][city]['latitude']
        longitude = self.data["cities"][city]['longitude']
        abbrev = self.data["cities"][city]['abbrev']
        weatherurl =f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,cloud_cover,rain,precipitation,wind_speed_10m,showers,apparent_temperature'
        if ((math.ceil(time.monotonic() - self.last_weather_check) % check_every)== 0) or self.initialise:
            self.last_weather_check = time.monotonic()
            try:
                time.sleep(self.sleep) #recommended to pause before sending requests from pico
                response = self.ssl_requests.get(weatherurl, timeout=2)
                data = json.loads(response.text)
                self.temperature = str(data['current']['temperature_2m'])
                self.temperature_missed = ''
            except Exception as e:
                self.temperature_missed = '*'
            label.text = f'{abbrev}:{self.temperature}{self.temperature_missed}c'
            self.center_label(label)

    def cat_facts(self, row):
        label = row["label"]
        last_cat_check = row["clock"]
        
        check_every = 300
        CatUrl="https://catfact.ninja/fact"
        
        if ((math.ceil(time.monotonic() - last_cat_check) % check_every)== 0) or self.initialise:
            try:
                row["clock"] = time.monotonic()
                time.sleep(self.sleep) #recommended to pause before sending requests from pico
                response = self.ssl_requests.get(CatUrl, timeout=2)
                data = json.loads(response.text)
                label.text = data.fact
            except Exception as e:
                # https ceretificate issues - may look at again if it works later
                print(e)
                pass