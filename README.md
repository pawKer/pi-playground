# piWorkspace

# Description
This is a repo for the things I play around with on Raspberry Pis. Use at your own risk because most of the stuff is experimental. Parts of code are found on the internet. The code is really messy since I was experimenting and mostly coding in nano lol. 

Some things in here include:
* a script for displaying the bitcoin price in USD on a Scroll pHAT HD led matrix
* some experiments to having internet radio on the pi that played music on a bluetooth speaker and displayed the song that is currently playing on the Scroll pHAT HD
* a web server implementation in Flask that runs on local host which provides useful stats about the pi, reads a humidity and temperature sensor, an interface to display text strings on the Scroll pHAT HD via the website, some Neopixel WS2812B LED Strip animations in python that can be triggered from the UI, an interface to control the color of the Neopixel LEDs via the UI and also to control the color three different sections of the led strip (some of these might be commented out and not fully working)
* a script that checks whether I am home by looking for the bluetooth of my mobile phone
* a script that can send a lot of emails really fast to spam someone
# Pre requisites:
* pip install pypbluez (requires aditional modules to be installed)
* pip install psutils

Commands: 

sudo apt-get install libbluetooth-dev

sudo pip install pybluez

sudo pip install psutil

sudo apt-get install build-essential python-dev git scons swig

git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
