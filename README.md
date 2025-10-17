# cp-led-matrix
Using a Raspberry Pi Pico, CircuitPython (+ javascript) and a standard LED Matrix create something people can have in their living room and use for whatever they can think of. This project contains all the code for loading onto the Raspberry Pi Pico.

## Background
Previously (10 years ago!) I had written [LED Matrix. Use your old Model A Raspberry Pi](https://rods-stuff.blogspot.com/2015/04/led-matrix-use-your-old-model-raspberry.html) and wanted to update the technology so I could give it to friends. This original proejct was very complex with a very wide range of technical expertise required to implement. So I set out to build something that friends could plug in and start using with no real technical expertise.  I haven't quite achived that, but it is much closer.

## Ambitions
I really had the following ambitions with this project
* Simple to build - extremly low entry to achive maximum results
* First and foremost - provide the ability to see the next three Trams coming at the end of my street (totally Melboure/Australia based). This deeply effects my family in the morning and its usefullness is the only reason I am allowed a LED matrix in the living/dining area's in the house.
  - The trams run on roads and have real time updates and one can be coming in 15 minutes, then 3 minutes later it is due in 5 minutes - it is traffic dependant.
* Make it easy to integrate with phone widgets - quick and easy to turn it on/off
* Make it easy to add new functionality

## What you need to buy / may have on hand
 
![Image of the LED Matrix put together](/README/LED_Matrix_Bits_sm.jpg)

I have zero affiliation with the company I am going to use for referecne, but my dealing with them have always been really good.
1. [Raspberry Pi Pico 2WH (Wireless WiFi, with Headers)](https://core-electronics.com.au/raspberry-pi-pico-2-wh-with-headers.html)
2. [5V DC 4A Fixed 2.1mm Tip Appliance Plugpack](https://core-electronics.com.au/5v-dc-4a-fixed-2-1mm-tip-appliance-plugpack-47354.html)
3. [DC Barrel Jack Adapter - Female](https://core-electronics.com.au/dc-barrel-jack-adapter-female-7392.html)
4. [RGB full-color LED matrix panel (2.5mm Pitch, 64x32 pixels)](https://core-electronics.com.au/rgb-full-color-led-matrix-panel-25mm-pitch-64x32-pixels.html) - this includes
    - 4a IDC to XH2.54 - from LED matrix to Pico GPIO Pins
    - 4b Power Supply Cable
5. Micro USB cable and power (phone charger more than enough)
6. Wire Strippers

> [!TIP]
> Check and recheck that the micro USB cable does data AND power. Some only do power. My first couple of weeks playing was spent telling Core-Electronics that they had sent me faulty devices. Turns out all 3 cables I tested with did not do data! They were very understanding.

## The build
We basically need to do the following
1. Get the Pico set up and ready to code on 
2. Install CircuitPython and dependencies
3. Build our LED matrix display 

## Get the Pico set up and ready to code on
### Start coding on the device and get used to writing code
Google _getting started raspberry pi pico_. Follow the bouncing ball on a tutorial like [Getting started with Raspberry Pi Pico](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico) which
* Install Thonny (Adafruit also has [Mu Editor](https://codewith.mu/), I thought Thonny was simpler)
* Using Thonny to code on the device

## Install CircuitPython and dependencies
You are going to delete all you have done on the Pico up until now and install CricuitPython
* I basically followed [Installing CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython)
* Use the package manager to install other libraries that this code requires (see below)
> [!NOTE]
> It did not always work exaclty as described in the tutorials, but was obvious with a bit of tinkering

Circuit Python Libraries to install (_Tools->Manage Packages_ in Thony menus)
* adafruit_httpserver (searching package manager in Thony, search for -> adafruit-circuitpython-httpserver)
* adafruit_hashlib (required on Adafruit Matrix Portal M4, not Pico -> adafruit-circuitpython-hashlib)
* adafruit_datetime (-> adafruit-circuitpython-datetime)
* adafruit_requests (-> adafruit-circuitpython-requests)
* adafruit__ntp (-> adafruit-circuitpython-ntp)
* adafruit_display_text (-> adafruit-circuitpython-display-text)
* adafruit_display_shapes (-> adafruit-circuitpython-display-shapes)

From this Repository
* Copy across Code.py and cfg
* Update cfg with your local wirelss name and password
* Copy across directories -> animation, data, img, saved, static, utils

You should now be able to run code.py, and be able to go to the 'website', the address will be in the Thonny IDE. but it won't do much until we hook up our LED Matrix

> [!NOTE]
> If you change the line in code.py to debug=True you will be able to see opening the website and any requests you make in the Thonny IDE.

```
    server = Server(pool, "/static", debug=False)
```

### Build our LED matrix display
Have a look at the picture above, it gives you a pretty good idea of where we are going.

1. Start with connecting the IDC ribbons pins to the Pico. Using the Pico diagram and the table below. (Disconnect it from the Micro USB to do this)
![Pico Pin Diagram](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-2-r4-pinout.svg)

```
| Function          | Wire   | GPIO Pin | Pico Pin |
|-------------------|--------|----------|----------|
| High R data       | Blue   | GP0      | 1        |
| High G data       | Green  | GP1      | 2        |
| High B data       | Yellow | GP2      | 4        |
| GND               | Orange | GND      | 3        |
| Low R data        | Red    | GP3      | 5        |
| Low G data        | Brown  | GP4      | 6        |
| Low B data        | Black  | GP5      | 7        |
| GND               | White  | GND      | 8        |
| A line selection  | Grey   | GP6      | 9        |
| B line selection  | Purple | GP7      | 10       |
| C line selection  | Blue   | GP8      | 11       |
| D line selection  | Green  | GP9      | 12       |
| E line selection  |        |          |          |
| CLOCK             | Yellow | GP10     | 14       |
| LATCH             | Orange | GP11     | 15       |
| Output Enable     | Red    | GP12     | 16       |
| GND               | Brown  | GND      | 18       |
```

2. Connect the other end of the IDC to the Matrix (make sure its to the right end)
Don't turn it on yet!

3. Affix the DC Barrel jack adaptor to the Power Supply Cable
I cut off the connectors and used the wire strippers - red to +ve, black to -ve

4. (Re)connect the Micro USB from your Pico to the Computer 
You will have unplugged it to connect the cables.
Stop Thonny IDE and restart code.py running

5. Turn on the Power to your Matix and cross your fingers.
Hopefully it all works and you can play with the WebSite IDE

## Other things to note
### Using widgets on your phone
You will notice the website always produces a URL every time you ask it to do something. The intention is NOT to use the website to drive the Matrix, but use those URL's in Pnone and tablet applications. I have an iPhone and the application Shortcuts, has a _Get Contents of URL_ shortcut. If you paste the contents of the _URL to Copy_ as the url - then the ponbe shortcut (which you can use as widgets on your homepage etc.) To drive the Matrix.  For example I have also used a Text Input in Shortcuts so I can nominate the time for any countdown from my widget.

I am fairly confident other operating systems, especially Andriod, has almost identical features.
### Adding new features
