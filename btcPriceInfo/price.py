import urllib, json
import time
import scrollphathd as sphd

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

while True:
  sphd.clear()
  sphd.show()
  f = urllib.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json")
  values = json.load(f)
  f.close()
  timeout = time.time() + 60
  curFloatPrice = values['bpi']['USD']['rate_float']
  if curFloatPrice > 7500:
    screenFlash()
  print 'Current price in USD: $',str(curFloatPrice)
  sphd.write_string('  USD ' + "%.2f" % curFloatPrice + " >>")
  sphd.set_brightness(0.1)
  while time.time() < timeout:
    sphd.show()
    sphd.scroll(1)
    time.sleep(0.1)
  
