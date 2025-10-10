#Native
import socketpool
import json
import wifi
import mdns
import time
import ssl
import rtc
import gc

#Added through Package Manager
from adafruit_httpserver import Request, Server, JSONResponse, FileResponse, MIMETypes
from adafruit_datetime import datetime, timedelta
import adafruit_requests
import adafruit_ntp

#Locally coded classes/files
from utils.LEDMatrix import LEDMatrixBasic, LEDMatrixStop
from utils.WordPunch import WordPunch #inherits from LEDMatrix
from utils.Animation import Animation #inherits from LEDMatrix
from utils.ThreeLines import ThreeLines #inherits from LEDMatrix
from utils.CountDown import CountDown #inherits from LEDMatrix
from utils.Score import Score #inherits from LEDMatrix
from utils.Images import Images #inherits from LEDMatrix
from utils.config import PMConfig


'''
==== SHARED FUNCTIONS ====
'''
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

'''
==== STARTUP ====
'''
try: 
    cfg = PMConfig('cfg')
    tz_offset = 0
    WIFI_SSID = cfg.getConfig('WIFI_SSID')
    WIFI_PASSWORD = cfg.getConfig('WIFI_PASSWORD')
    HOSTNAME = cfg.getConfig('HOSTNAME')
    timezonedb_api_key = cfg.getConfig('timezonedb_api_key')
    timezonedb_zone = cfg.getConfig('timezonedb_zone')
    data = cfg.get_all_matrix_config() #does all the file reads needed

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
    server = Server(pool, "/static", debug=False)
    server.headers = {"Access-Control-Allow-Origin": "*",}

    #Get local time offset
    tz_offset = get_local_offset()

    # Start running the server
    server.start(str(wifi.radio.ipv4_address))

    '''
    Default matrix
    '''
    dis = LEDMatrixBasic(tz_offset, requests, ssl_requests, data, {"text":f"address is http://{HOSTNAME}.local:5000","color":"White"})
    
except Exception as e:
    ctime = (datetime.now() + timedelta(seconds= tz_offset)).timetuple()
    error_message = f"An error occurred at startup {ctime.tm_hour:02}:{ctime.tm_min:02} {e} - RESTART DEVICE"
    dis = LEDMatrixBasic(0, '', '', {}, {"text":error_message,"color":"Red"})


'''
==== HTTP SERVER ====
'''
MIMETypes.configure(
    default_to="text/plain",
    # Unregistering unnecessary MIME types can save memory
    keep_for=[".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico"],
    # If you need to, you can add additional MIME types
    register={".foo": "text/foo", ".bar": "text/bar"},
)

# You don't have to add any routes for servicng files from /static, by default the server will serve files
# and it appears it serves index.html by default

@server.route("/getdata")
def base(request: Request):
    return JSONResponse(request, data)

@server.route("/loadjson")
def base(request: Request):
    jsonparam = request.query_params["json"]
    decoded_json = json.loads(decode_pico(jsonparam))
    m_name = decoded_json["name"]
    global dis
    if m_name == "Stop":
        dis = LEDMatrixStop(tz_offset, requests, ssl_requests, data, {})
    elif m_name == "WordPunch":
        dis = WordPunch(tz_offset, requests, ssl_requests, data, decoded_json)
    elif m_name == "Animation":
        dis = Animation(tz_offset, requests, ssl_requests, data, decoded_json)
    elif m_name == "ThreeLines":
        dis = ThreeLines(tz_offset, requests, ssl_requests, data, decoded_json)
    elif m_name == "3LinesFile":
        saved_json = ThreeLines.load_from_file(decoded_json["file"])
        dis = ThreeLines(tz_offset, requests, ssl_requests, data, saved_json)
    elif m_name == "Images":
        dis = Images(tz_offset, requests, ssl_requests, data, decoded_json)
    elif m_name == "CountDown":
        dis = CountDown(tz_offset, requests, ssl_requests, data, decoded_json)
    elif m_name == "Score":
        if decoded_json["mode"] == 'load':
            dis = Score(tz_offset, requests, ssl_requests, data, decoded_json)
        else:
            dis.update(decoded_json)
    return JSONResponse(request, {})


'''
==== RUNNING ====
'''
while True:
    try:
        server.poll()
    except Exception as e:
        # We have occaisionally seen issues with the poll throwing errors for no reason, adding this in to see if
        # it syabailses things
        gc.collect()

    try:
        dis.poll()
    except Exception as e:
        # This will be errors with designed functionality
        ctime = (datetime.now() + timedelta(seconds= tz_offset)).timetuple()
        error_message = f"An error occurred at {ctime.tm_hour:02}:{ctime.tm_min:02} {e} - TRY ANOTHER FUNCTION, or RESTART DEVICE"
        dis = LEDMatrixBasic(tz_offset, requests, ssl_requests, data, {"text":error_message,"color":"Red"})      

''' 
    server.poll()
    dis.poll()
'''
