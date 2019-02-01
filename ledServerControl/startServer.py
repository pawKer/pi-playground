import os
import bluetooth
from flask import Flask, render_template, request
import scrollphathd as sphd
import time
import psutil
app = Flask(__name__)

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
  print cpu_percent, ram_percent, disk_percent
  return render_template('index.html', uptime=tuna, home=home, cpu_percent=cpu_percent, ram_percent=ram_percent,disk_percent=disk_percent)

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
def display_text(text):
    sphd.clear()
    sphd.show()
    timeout = time.time() + 30
    sphd.write_string(text)
    sphd.set_brightness(1)
    while time.time() < timeout:
        sphd.show()
      	sphd.scroll(1)
    	time.sleep(0.1)
    sphd.clear()
    sphd.show()
def screenFlash():
    i=1
    while i <= 5:
      sphd.fill(1,0,0,17,7)
      sphd.set_brightness(1)
      sphd.show()
      time.sleep(0.2)
      screenClear()
      i=i+1
def screenClear():
    sphd.clear()
    sphd.show()

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
