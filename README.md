# cp-led-matrix
Using a Raspberry Pi Pico, CircuitPython (+ javascript) and a standard LED Matrix create something people can have in their living room and use for whatever they can think of. This project contains all the code for loading onto the Raspberry Pi Pico.

## Background
Previously (10 years ago!) I had written [LED Matrix. Use your old Model A Raspberry Pi](https://rods-stuff.blogspot.com/2015/04/led-matrix-use-your-old-model-raspberry.html) and wanted to update the technology so I could give it to friends. This original proejct was very complex with a very wide range of technical expertise required to implement. So I set out to build something that friends could plug in and start using with no real technical expertise.  I haven't quite achived that, but it is much closer.

## Ambitions
I really had the following ambitions with this project
* Simple to build - extremly low entry to achive maximum results
* First and foremost - provide the ability to see the next three Trams coming at the end of my street (totally Melboure/Australia based). This deeply effects my family in the morning and its usefullness is the only reason I am allowed a LED matrix in the living/dining area's in the house.
  - The trams run on raods and have real time updates and one can be coming in 15 minutes, then 3 minutes later it is due in 5 minutes - it is traffic dependant.
* Make it easy to integrate with phone widgets - quick and easy to turn it on/off
* Make it easy to add new functionality

## What you need to buy / may have on hand
I have zero affiliation with the company I am going to use for referecne, but my dealing with them have always been really good.
* [Raspberry Pi Pico 2WH (Wireless WiFi, with Headers)](https://core-electronics.com.au/raspberry-pi-pico-2-wh-with-headers.html){:target="_blank"}
* [RGB full-color LED matrix panel (2.5mm Pitch, 64x32 pixels)](https://core-electronics.com.au/rgb-full-color-led-matrix-panel-25mm-pitch-64x32-pixels.html){:target="_blank"}
  - The above comes with all the cables required for powering and hooking up the Pico to the LED Matrix so you can drive it
* [5V DC 4A Fixed 2.1mm Tip Appliance Plugpack](https://core-electronics.com.au/5v-dc-4a-fixed-2-1mm-tip-appliance-plugpack-47354.html){:target="_blank"}
* [DC Barrel Jack Adapter - Female](https://core-electronics.com.au/dc-barrel-jack-adapter-female-7392.html){:target="_blank"}

### Other bits and piece / Tools
* [Jumper Wire 10cm Ribbon (F/F)](https://core-electronics.com.au/female-to-female-dupont-line-40-pin-10cm-24awg.html){:target="_blank"}
  - I ended up powering the Pico off the cables leading into the matrix, and I basically cut these up to connect to the Pico. This can be done in a WIDE variety of ways.
* Micro USB cable. One of the thousands you have left over from years of non-standard powering of device. This is for plugging into you Pico to load the code / Test
> [!TIP]
> Check and recheck that the cable does data AND power. Some only do power. My first couple of weeks playing was spent telling Core-Electronics that they had sent me faulty devices. Turns out all 3 cables I tested with did not do data!

## The build
We basically need to do the following
1. Get the Pico set up and ready to code on
2. Build our LED matrix display
3. Load the code onto the Pico and configure for your local network

Circuit Python Libraries to install
* adafruit_httpserver (searching package manager in Thony, search for -> adafruit-circuitpython-httpserver)
* adafruit_hashlib (required on Adafruit Matrix Portal M4, not Pico -> adafruit-circuitpython-hashlib)
* adafruit_datetime (-> adafruit-circuitpython-datetime)
* adafruit_requests (-> adafruit-circuitpython-requests)
* adafruit__ntp (-> adafruit-circuitpython-ntp)
* adafruit_display_text (-> adafruit-circuitpython-display-text)
* adafruit_display_shapes (-> adafruit-circuitpython-display-shapes)

Fonts
Download from https://github.com/adafruit/circuitpython-fonts/releases
