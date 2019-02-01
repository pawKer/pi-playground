#!/usr/bin/python

import bluetooth
import time
import scrollphathd as sphd
import urllib,json

# Python script to check if my phone is home by checking if it finds
# it on bluetooth. If it is home, it displays BTC information.
# Continous flashes = BTC price is lower than $5000
# Thanks to github.com/paulbarber for the bluetooth check code


def screenFlash():
  sphd.fill(1,0,0,17,7)
  sphd.show()
  time.sleep(0.2)
  screenClear()
  sphd.fill(1,0,0,17,7)
  sphd.show()
  time.sleep(0.2)
  screenClear()
  sphd.fill(1,0,0,17,7)
  sphd.show()
  time.sleep(0.2)
  screenClear()
  time.sleep(1)
def screenClear():
  sphd.clear()
  sphd.show()
def displayBtcPrice():
  screenClear()
  f = urllib.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json")
  values = json.load(f)
  f.close()
  timeout = time.time() + 30
  curFloatPrice = values['bpi']['USD']['rate_float']
  if curFloatPrice < 5000:
     while True:
       screenFlash()
       time.sleep(3)
  print 'Current price in USD: $',str(curFloatPrice)
  sphd.write_string('  USD ' + "%.2f" % curFloatPrice + " >>")
  sphd.set_brightness(0.1)
  while time.time() < timeout:
    sphd.show()
    sphd.scroll(1)
    time.sleep(0.1)
  screenClear()

print "In/Out Board"

home=False

while True:
    
    print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

    result = bluetooth.lookup_name('78:7E:61:80:2B:01', timeout=5)
    
    if (result != None):
        print "Rares: in"
        if home == False:
            sphd.write_string(" >>> Welcome home, Rares ! ")
            sphd.set_brightness(0.3)
            timeout = time.time() + 60
            while time.time() < timeout:
                sphd.show()
                sphd.scroll(1)
                time.sleep(0.1)
            screenClear()
            home = True
    else:
        print "Rares: out"
        time.sleep(15)
        home = False

    if home == True:
        displayBtcPrice()

