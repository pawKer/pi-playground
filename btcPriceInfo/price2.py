import urllib, json
import time
import scrollphathd as sphd
from scrollphathd.fonts import font5x5

while True:
  sphd.clear()
  sphd.show()
  f = urllib.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json")
  values = json.load(f)
  f.close()
  timeout = time.time() + 60
  curFloatPrice = values['bpi']['USD']['rate_float']
  print 'Current price in USD: $',str(curFloatPrice)
  sphd.write_string("%.2f" % curFloatPrice,x=0,y=1,font=font5x5)
  sphd.set_brightness(0.1)
  while time.time() < timeout:
    sphd.show()
    #sphd.scroll(1)
    time.sleep(0.1)
  
