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

I have zero affiliation with the company I am going to use for reference, but my dealing with them have always been really good.
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
* Use Thonny to code on the device and understand the principles. I just got the led on the Pico flashing before I moved on.

## Install CircuitPython and dependencies
You are going to delete all you have done on the Pico up until now and install CricuitPython
* I basically followed [Installing CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython)
* Use the package manager to install other libraries that this code requires (see below)
> [!NOTE]
> It did not always work exactly as described in the tutorials, but was obvious with a bit of tinkering

CircuitPython Libraries to install (_Tools->Manage Packages_ in Thonny menus)
* adafruit_httpserver (searching package manager in Thony, search for -> adafruit-circuitpython-httpserver)
* adafruit_hashlib (required on Adafruit Matrix Portal M4, not Pico -> adafruit-circuitpython-hashlib)
* adafruit_datetime (-> adafruit-circuitpython-datetime)
* adafruit_requests (-> adafruit-circuitpython-requests)
* adafruit_ntp (-> adafruit-circuitpython-ntp)
* adafruit_display_text (-> adafruit-circuitpython-display-text)
* adafruit_display_shapes (-> adafruit-circuitpython-display-shapes)

From this Repository
* Copy across Code.py and cfg
* Update cfg with your local wirelss name and password
* Register (https://timezonedb.com/), then Update cfg with your timezonedb_api_key. Micopython and Circuitpython are missing ALOT of python libraries and this helps us manage accurate time.
* Copy across directories -> animation, data, img, saved, static, utils

You should now be able to run code.py, and be able to go to the 'website', the address will be in the Thonny IDE. It won't do much until we hook up our LED Matrix

> [!NOTE]
> If you change the line in code.py to debug=True you will be able to see opening the website and any requests you make in the Thonny IDE.

```
    server = Server(pool, "/static", debug=False)
```

### Build our LED matrix display
Have a look at the picture above, it gives you a pretty good idea of where we are going.

1. Start with connecting the IDC ribbons pins to the Pico. Using the Pico diagram and the table below. (Disconnect it from the Micro USB to do this)
![Pico Pin Diagram](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-2-r4-pinout.svg)

Wire (if you are not colour blind) to Pico Pin is the easiest way to go.
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
Stop Thonny IDE and restart code.py

5. Turn on the Power to your Matix and cross your fingers.
Hopefully it all works and you can play with the Website driver

## Other things to note
### Using widgets on your phone
You will notice the website always produces a URL every time you ask it to do something. The intention is NOT to use the website to drive the Matrix, but use those URL's in widgets on the iPhone and tablet applications. I have an iPhone and the application _Shortcuts_ has a _Get Contents of URL_ shortcut. If you paste the contents of the _URL to Copy_ as the url - then the iPhone shortcut (which you can add as widgets on your homepage etc.) to drive the Matrix.  For example I have also used a Text Input in Shortcuts so I can nominate the time for any countdown from my widget.

I am fairly confident other operating systems, especially Andriod, has almost identical apps/features.

### Adding new features
A fair bit of effort went into making this project easily extendable. Micropython and CircuitPythons limited python libraries prevented this being a project where you could just drop new files and they would be dynamically loaded. However, it is still fairly simple to add new functionality.

When looking at adding new features, follow along with CountDown as an example - hard to go wrong. Most things will work of you follow conventions. There are 2 main parts, a web front end to choose functionality, and driving the matrix using Circuitpython based on the request from the web front end. 

#### Front End - web interface
Basically three area's need updating in the static directory:
1. Create a new Javascript file (copy count_down.js and rename). Rename x_process and x_load to your new feature name (identical to step 3)
 - delete pause_countdown unless you need similar funtionality which inegrates with a running feature
2. Add js file in index.html header
3. Include new feature as an option in the dropdown for id _rgb-function-to-run_
 - the buttons use dynamic javascript (window context) to run fucntions based on the value selected in the dropdown 

and then start coding (by example) in your new javascript file. Its basically doing domain object injection. See what I have done, and copy. Its not supposed to be a beautiful interface, but functional so you can generate the url's to put in widgets.

I found coding javascript locally (file system) while running Thonny meant that the json gets loaded, but I didn't have to restart Thonny all the time. To do this I temporarily hacked the fetch in _index.js_ to not be relative. DON"T FORGET to turn it back.

#### Driving the matrix
This is very similar to the front end. Again use CountDown:
1. Copy CountDown.py (in the utils directory). Rename it and rename the Class in the file
2. Update code.py. 
 - import the new Class - near the top
 - The route for loadjson has an _if / else if_ that needs to be added to. 

and then start coding. Circuitpython doco is pretty good and it does some amazing things. When you start getting fancy you are likely to need to add more packages for functionality. Thonny does this easily (see section above when setting up Thonny).

I found coding directly through Thonny onto the device the best way as you got imnmediate feedback. I also removed the try's in the while / true loop as it made it much easier to find issues.

### Only 1 power source
![Image of the LED Matrix with one power source](/README/Refined.jpg)
At some point, we plug it and use it, and stop playing with it. When that point comes, it is worth driving the Pico off the 5V power source instead of a separate power source. The above diagram shows 
1. the connection from the +ve and -ve wires to 
2. pin 39 (+ve) and pin 38 (-ve/GRND)
3. My 3D printed cover for the matrix.
> [!CAUTION]
> NEVER have your Pico plugged into a micro USB AND running off a separate power source. This can break your Pico.

There is also a led-matrix.stl file, which I used to create a simple box for the LED-Matrix. Unfortuantely my 3d printer was only 20cm by 20cm, so I had to do half at a time, thus the dodgy fit.

### Examples of some of the features
#### Scoreboard
![Scoreboard](/README/ScoreBoard.jpg)
#### Countdown
It can be paused too!
![CountDown](/README/CountDown.jpg)
#### Next 3 Trams
MOST important because I can have it in the living room due to this functionality
![NextTramsAndTime](/README/NextTramsAndTime.jpg)
#### Other features
* Weather is available, but I found it made the system unstable. I never figured out of it was the poor network connection in the living room, the API I was using (needed ssl connection) or any other reason. Try it out, but you will have to load your city into cities.json in the data directory. I found co-ordinates using google maps. 
* Text Display. Next 3 Trams uses something called ThreeLines (in python) and Text Display in the front end. It allows you to display up to three lines on the matrix and is exceptionally flexible with what you can do with it - Just play with it, and you can add Weather back as an option. I only removed it from the front end. (update javascript function `text_display_line_load` in `text_display.js`)
* Scrolling Text - part of Display Text / ThreeLines
* Clock - part of Display Text / ThreeLines
* Images and animations need to be pre-loaded onto the Pico, but just loading the files using underscores in the filename will have them appear in the options. For best results, make them 64 x 32 bit images. Lots of websites out there to help you.

