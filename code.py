'''
Web related imports
'''
import os
import socketpool
import json
import wifi
import mdns
from adafruit_httpserver import Request, Server, JSONResponse, FileResponse
from adafruit_datetime import datetime, timedelta
import adafruit_requests
import ssl

'''
Matrix related imports
'''
import adafruit_ntp
import rtc

from utils.LEDMatrix import LEDMatrixBasic
from utils.WordPunch import WordPunch #inherits from LEDMatrix
from utils.Animation import Animation #inherits from LEDMatrix
from utils.ThreeLines import ThreeLines #inherits from LEDMatrix
from utils.CountDown import CountDown #inherits from LEDMatrix
from utils.Images import Images #inherits from LEDMatrix
from utils.config import PMConfig
import time

'''
Pico specific code
'''
cfg = PMConfig('cfg')
tz_offset = 0
WIFI_SSID = cfg.getConfig('WIFI_SSID')
WIFI_PASSWORD = cfg.getConfig('WIFI_PASSWORD')
HOSTNAME = cfg.getConfig('HOSTNAME')
timezonedb_api_key = cfg.getConfig('timezonedb_api_key')
timezonedb_zone = cfg.getConfig('timezonedb_zone')

# no decoding availbale in pico/adfruit circuit python libraries
def decode_pico(url):
    basic_decoding = {"%20":" ","%26":"&", "%3D":"=", "%23":"#", "%2F":"/", "%2B":"+", "%25":"%", "%3F":"?", "%3A":":", "%2C":",", "%27":"'", "%21":"!", "%2A":"*", "%28":"(", "%29":")", "%22":"\"", "%7B":"{", "%7D":"}", "%5B":"[", "%5D":"]"}
    for dec in basic_decoding.keys():
        url = url.replace(dec, basic_decoding[dec])
    return url

def get_local_offset():
    timeurl = f'https://api.timezonedb.com/v2.1/get-time-zone?key={timezonedb_api_key}&format=json&by=zone&zone={timezonedb_zone}'
    response = ssl_requests.get(timeurl)
    data = json.loads(response.text)
    return int(data['gmtOffset'])

# creating a hostname for local server
mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = HOSTNAME
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=5000)

print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected to {WIFI_SSID} on {wifi.radio.ipv4_address} as http://{HOSTNAME}.local:5000")
pool = socketpool.SocketPool(wifi.radio)

# for connecting to external API's over http
requests = adafruit_requests.Session(pool)

# for connecting to external API's over https
ssl_context = ssl.create_default_context()
ssl_requests = adafruit_requests.Session(pool,ssl_context)

# set the time on the pico to current GMT
ntp = adafruit_ntp.NTP(pool)
rtc.RTC().datetime = ntp.datetime

'''
Local server and API related code
'''
# Set up http server (I have index.html in there)
server = Server(pool, "/static", debug=True)
server.headers = {"Access-Control-Allow-Origin": "*",}

@server.route("/")
def base(request: Request):
    #Not sure why, but when using HOSTNAME index.js seemed not to work without this
    return FileResponse(request, "index.html")

@server.route("/stop")
def base(request: Request):
    dis.BlankScreen()
    return JSONResponse(request, {})

@server.route("/getcomponentdata")
def base(request: Request):
    if m_name == "Animation":
        obj = Animation.get_data()
    return JSONResponse(request, obj)

@server.route("/getdata")
def base(request: Request):
    contents = os.listdir('./saved')
    saved = []
    for item in contents:
        saved.append(item.replace('.json', '').replace('_', ' '))
    saved.sort()
    contents = os.listdir('./img')
    images = []
    for item in contents:
        images.append(item.replace('.bmp', '').replace('_', ' '))
    images.sort()
    contents = os.listdir('./animation')
    animations = []
    for item in contents:
        animations.append(item.replace('_', ' '))
    animations.sort()
    return JSONResponse(request, {"saved":saved, "images":images, "animations":animations, "colors":dis.colors, "cities":dis.cities})

@server.route("/loadjson")
def base(request: Request):
    jsonparam = request.query_params["json"]
    decoded_json = json.loads(decode_pico(jsonparam))
    m_name = decoded_json["name"]
    global dis
    if m_name == "WordPunch":
        dis = WordPunch(tz_offset, requests, ssl_requests, decoded_json)
    elif m_name == "Animation":
        dis = Animation(tz_offset, requests, ssl_requests, decoded_json)
    elif m_name == "ThreeLines":
        dis = ThreeLines(tz_offset, requests, ssl_requests, decoded_json)
    elif m_name == "3LinesFile":
        saved_json = ThreeLines.load_from_file(decoded_json["file"])
        dis = ThreeLines(tz_offset, requests, ssl_requests, saved_json)
    elif m_name == "Images":
        dis = Images(tz_offset, requests, ssl_requests, decoded_json)
    elif m_name == "CountDown":
        dis = CountDown(tz_offset, requests, ssl_requests, decoded_json)
    return JSONResponse(request, {})

#Get local time offset
tz_offset = get_local_offset()

# Start running the server
server.start(str(wifi.radio.ipv4_address))

'''
Matrix related code
'''
dis = LEDMatrixBasic(tz_offset, requests, ssl_requests, {"text":f"address is http://{HOSTNAME}.local:5000","color":"White"})

while True:
    try:
        server.poll()
        dis.poll()
    except Exception as e:
        ctime = (datetime.now() + timedelta(seconds= tz_offset)).timetuple()
        error_message = f"An error occurred at {ctime.tm_hour:02}:{ctime.tm_min:02} {e}"
        dis = LEDMatrixBasic(tz_offset, requests, ssl_requests, {"text":error_message,"color":"Red"})
'''
    server.poll()
    dis.poll()
''' 




