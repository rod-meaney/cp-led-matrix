'''
Web related imports
'''
import socketpool
import os
import json
import wifi
import mdns
import microcontroller
import traceback
from adafruit_httpserver import Request, Response, Server, JSONResponse, FileResponse
from adafruit_datetime import datetime, timedelta
import adafruit_requests
import ssl
from utils.web import PMWeb

'''
Matrix related imports
'''
import adafruit_ntp
import rtc

from utils.matrix import PMMatrix
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

@server.route("/home")
def base(request: Request):
    return Response(request, web.webpage(microcontroller.cpu.temperature), content_type="text/html")

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

@server.route("/loadsaved")
def base(request: Request):
    ftype = request.query_params["type"]
    file = request.query_params["file"]
    if ftype == 'img':
        dis.BlankScreen()
        dis.ShowImage(f'img/{file}.bmp')
    elif ftype == 'animation':
        dis.NewMatrix({"name":"Animation", "mins":0, "directory": file})
    else:
        filename = f'./saved/{file}.json'
        with open(filename, "r") as file:
            data = json.load(file)
        dis.NewMatrix(data)
    return JSONResponse(request, {})

@server.route("/stop")
def base(request: Request):
    dis.BlankScreen()
    return JSONResponse(request, {})

@server.route("/loadmsg")
def base(request: Request):
    text = request.query_params["text"]
    color = request.query_params["color"]
    mins = int(request.query_params["mins"])
    dis.NewMatrix({"name":"CenteredText", "mins":mins, "distext": text.replace('%20', ' '), "color":color})
    return JSONResponse(request, {})

@server.route("/loadjson")
def base(request: Request):
    jsonparam = request.query_params["json"]
    decoded_json = decode_pico(jsonparam)
    print(decoded_json)
    dis.NewMatrix(json.loads(decoded_json))
    return JSONResponse(request, {})

@server.route("/loadcity")
def base(request: Request):
    city = decode_pico(request.query_params["city"])
    dis.NewMatrix({"name":"TwoLines", "mins":0,"top_line":{"type":"scroll", "color":"Blue", "text":"Local temperature", "data":{}},"bot_line":{"type":"weather", "color":"Blue", "data":{"city": city}}})
    return JSONResponse(request, {})

@server.route("/update")
def base(request: Request):
    print(request.query_params)
    data = {
        "temperature": microcontroller.cpu.temperature,
        "frequency": microcontroller.cpu.frequency,
    }
    return JSONResponse(request, data)

#Get local time offset
tz_offset = get_local_offset()

# Start running the server
server.start(str(wifi.radio.ipv4_address))

'''
Matrix related code
'''
dis = PMMatrix(tz_offset, requests, ssl_requests)
dis.NewMatrix({"name":"CenteredText", "mins":5, "distext": f"address is http://{HOSTNAME}.local:5000", "color":"White"})

while True:
    try:
        server.poll()
        dis.poll()
    except Exception as e:
        ctime = (datetime.now() + timedelta(hours= tz_offset)).timetuple()
        error_message = f"An error occurred at {ctime.tm_hour:02}:{ctime.tm_min:02} {e}"
        dis.CenteredText(error_message, "Red")
'''
    server.poll()
    dis.poll()
''' 