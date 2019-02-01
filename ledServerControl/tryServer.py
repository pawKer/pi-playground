import os
import bluetooth
from flask import Flask, render_template, request
#import Adafruit_DHT as dht
#import scrollphathd as sphd
import time
import psutil
from neopixel import *
import argparse
app = Flask(__name__)

# ========================================
# FOR setPixelColorRGB RGB is actually GRB WTFFF
# =======================================

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, r, g, b, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        
        strip.setPixelColorRGB(i, g, r, b)
        strip.show()
        time.sleep(wait_ms/1000.0)

def fillWithColor(strip, r, g ,b):
  for i in range(strip.numPixels()):
    strip.setPixelColorRGB(i, g, r, b)
  strip.show()

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
    
def romFlag(strip, wait_ms=20, iterations=1):
  for i in range(1,90,1):
    strip.setPixelColorRGB(i,0,255,0)
  for i in range(90,160,1):
    strip.setPixelColorRGB(i,255,255,0)
  for i in range(160,LED_COUNT,1):
    strip.setPixelColorRGB(i,0,0,255)
  strip.show()
def neonLights(strip):
  for i in range(19,69,1):
    strip.setPixelColorRGB(i, 255, 0, 94)
  for i in range(69,149,1):
    strip.setPixelColorRGB(i, 13, 247, 255)
  for i in range(149,200,1):
    strip.setPixelColorRGB(i, 255, 0, 94)
  for i in range(200,LED_COUNT,1):
    strip.setPixelColorRGB(i, 0, 0, 0)
  strip.show()
def fillBotShelf(strip, r, g, b):
  for i in range(19,69,1):
    strip.setPixelColorRGB(i, g, r, b)
  strip.show()
def fillMidShelf(strip, r, g, b):
  for i in range(69,149,1):
    strip.setPixelColorRGB(i, g, r, b)
  strip.show()
def fillTopShelf(strip, r, g, b):
  for i in range(149,200,1):
    strip.setPixelColorRGB(i, g, r, b)
  strip.show()
  
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

@app.route('/')
def index():
  f = os.popen('uptime')
  now = f.read()
  tuna = now[12:20]
  tuna = tuna.strip()
  tuna = tuna.replace(",","")
  result = bluetooth.lookup_name('78:7E:61:80:2B:01', timeout=5)
  home = ""
  if (result != None):
    home="Rares is currently home."
  else:
    home="Rares is currently away from home."

  cpu_percent=psutil.cpu_percent(interval=1)
  ram_percent=psutil.virtual_memory().percent
  disk_percent=psutil.disk_usage('/').percent
  #TEMPERATURE SENSOR
  #h,t = dht.read_retry(dht.DHT22, 4)
  #tempHum = 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h)
  tempHum = ''	
  print cpu_percent, ram_percent, disk_percent
  return render_template('index.html', uptime=tuna, home=home, cpu_percent=cpu_percent, ram_percent=ram_percent,disk_percent=disk_percent, tempHum=tempHum)

@app.route('/leds')
def ledControl():
  return render_template('led.html')
@app.route('/handle_post', methods=['POST'])
def my_form_post():

   # text = request.form['text']
   # processed_text = text.upper()
   receivedText = " >>> " + request.form['text']
   app.logger.info("Received text: " + receivedText)
   screenFlash()
   display_text(receivedText)

   #return render_template('index.html', inputText = processed_text)
   return "Text displayed!"
@app.route('/ping', methods=['GET'])
def ping():
  app.logger.info("Received ping request")
  #return json.dumps({'status':OK}), 200, {'ContentType':'application/json'}
  return render_template('index.html')
@app.route("/romFlag")
def triggerRomFlag():
  romFlag(strip)
  return "/"
@app.route("/neonLights")
def triggerNeonLights():
  neonLights(strip)
  return "/"
@app.route("/colwipe")
def triggerColorWipe():

  colorWipe(strip, 255, 0, 0)  # Red wipe
  colorWipe(strip, 0, 0, 255)  # Blue wipe
  colorWipe(strip, 0, 255, 0)  # Green wipe
  colorWipe(strip, 0,0,0, 0)
  return "/"  

@app.route("/rainbow")
def triggerRainbow():
  rainbow(strip)
  colorWipe(strip, Color(0,0,0), 5)
  return "/"

@app.route("/theaterRainbow")
def triggerTheaterChaseRainbow():
    theaterChaseRainbow(strip)
    return "/"

@app.route("/fill", methods=['GET','POST'])
def triggerFill():
  request_json = request.get_json()
  redValue=request_json.get('r')
  greenValue=request_json.get('g')
  blueValue=request_json.get('b')
  #fillWithColor(strip, 0, 0, 0)
  fillWithColor(strip, redValue, greenValue, blueValue)
  return "/"
@app.route("/fillTopShelf", methods=['POST'])
def triggerFillTopShelf():
  request_json = request.get_json()
  redValue=request_json.get('r')
  greenValue=request_json.get('g')
  blueValue=request_json.get('b')
  #fillTopShelf(strip, 0, 0, 0)
  fillTopShelf(strip, redValue, greenValue, blueValue)
  return "/"
@app.route("/fillMidShelf", methods=['POST'])
def triggerFillMidShelf():
  request_json = request.get_json()
  redValue=request_json.get('r')
  greenValue=request_json.get('g')
  blueValue=request_json.get('b')
  #fillWithColor(strip, 0, 0, 0)
  fillMidShelf(strip, redValue, greenValue, blueValue)
  return "/"
@app.route("/fillBotShelf", methods=['POST'])
def triggerFillBotShelf():
  request_json = request.get_json()
  redValue=request_json.get('r')
  greenValue=request_json.get('g')
  blueValue=request_json.get('b')
  #fillBotShelf(strip, 0, 0, 0)
  fillBotShelf(strip, redValue, greenValue, blueValue)
  return "/"

if __name__ == '__main__':
  # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    app.run(debug=True, host='0.0.0.0')


