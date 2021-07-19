﻿# RGB LED Strip 
 
 This is just a fun little project I did between my 3rd and 4th years to spruce up my Uni room a bit.
 An ESP32 running MicroPython is used to control a 12V RGB LED strip using PWM.
 The ESP32 hosts a webserver connected to the local netowork that can receive POST requests to vary the settings and behaviour of the strip.
 The lights can be set to a static value, or flash or fade between an arbitrary number of colours.
 
 
 ## Directory Structure 
 
 ### Hardware
 Contains a system block diagram and an Eagle schematic file for the ESP32 hardware.
 
 ### JSLibrary
 Contains a JavaScript library that can be incoporated into any basic HTML/CSS/JavaScript site.
 Also has a HTML page desiged to test the script.
 
 ### uPythonCode
 Contains the MicroPython code running on the ESP32.
 Also contains a directory of hosted test scripts that send a series of requests to the ESP32.
 
