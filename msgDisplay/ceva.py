from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import time
import logging
from scrollphathd.fonts import font5x5
import scrollphathd as sphd
from threading import Thread
from Queue import Queue


DISPLAY_BAR = True
#Brightness of the seconds bar and text
BRIGHTNESS = 0.1

#Uncomment to rotate
#sphd.rotate(180)
queue = Queue()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
class Clock(object):
  logging.debug("THIS CLASS GETS COMPILEDISH")
  def runClock():
    while True:
      sphd.clear()

      # Grab the "seconds" component of the current time
      # and convert it to a range from 0.0 to 1.0
      float_sec = (time.time() % 60) / 59.0

      # Multiply our range by 15 to spread the current
      # number of seconds over 15 pixels.
      #
      # 60 is evenly divisible by 15, so that
      # each fully lit pixel represents 4 seconds.
      #
      # For example this is 28 seconds:
      # [x][x][x][x][x][x][x][ ][ ][ ][ ][ ][ ][ ][ ]
      #  ^ - 0 seconds                59 seconds - ^
      seconds_progress = float_sec * 15

      if DISPLAY_BAR:
        # Step through 15 pixels to draw the seconds bar
        for y in range(15):
          # For each pixel, we figure out its brightness by
          # seeing how much of "seconds_progress" is left to draw
          # If it's greater than 1 (full brightness) then we just display 1.
          current_pixel = min(seconds_progress, 1)

          # Multiply the pixel brightness (0.0 to 1.0) by our global brightness value
          sphd.set_pixel(y + 1, 6, current_pixel * BRIGHTNESS)

          # Subtract 1 now we've drawn that pixel
          seconds_progress -= 1

          # If we reach or pass 0, there are no more pixels left to draw
          if seconds_progress <= 0:
            break

      else:
        # Just display a simple dot
        sphd.set_pixel(int(seconds_progress), 6, BRIGHTNESS)

      # Display the time (HH:MM) in a 5x5 pixel font
      sphd.write_string(
        time.strftime("%H:%M"),
        x=0, # Align to the left of the buffer
        y=0, # Align to the top of the buffer
        font=font5x5, # Use the font5x5 font we imported above
        brightness=BRIGHTNESS # Use our global brightness value
      )

      # int(time.time()) % 2 will tick between 0 and 1 every second.
      # We can use this fact to clear the ":" and cause it to blink on/off
      # every other second, like a digital clock.
      # To do this we clear a rectangle 8 pixels along, 0 down,
      # that's 1 pixel wide and 5 pixels tall.
      if int(time.time()) % 2 == 0:
        sphd.clear_rect(8, 0, 1, 5)

      # Display our time and sleep a bit. Using 1 second in time.sleep
      # is not recommended, since you might get quite far out of phase
      # with the passing of real wall-time seconds and it'll look weird!
      #
      # 1/10th of a second is accurate enough for a simple clock though :D
      sphd.show()
      time.sleep(0.1)

class MessageListener(object):
  logging.debug("EXECUTING THIS MOFOCKING CLASS")
  app = Flask("Message listener")
  account_sid = "ACcd55cecad9957ea8780354bb06c7590d"
  auth_token = "8511ba7054532277db3dc8b144693777"
  #client = TwilioRestClient(account_sid, auth_token)
  def __init__(self):
    logging.debug("CONSTRUCTOR CALLED")
    self.app = Flask("Message listener") 
  logging.debug("AFTER CONSTRUCT")
  
  def run(self):
    self.app.run()
  logging.debug("wants to go here")
@MessageListener.app.route("/sms", methods=['POST'])
def listen():
  """Respond to incoming calls with a simple text message."""
  newMsg = 1
  fromNo = request.form['From']
  msgBdy = request.form['Body']
  print "From:", fromNo
  print "Saying:", msgBdy
  queue.put(msgBdy)
  #resp = MessagingResponse()
  #resp.message("Message displayed on pi ! You can send a new one now !")
  print str(resp)
  return str(resp)

class MessageProcessor(object):
  logging.debug("THIS CLASS GETS COMPILEDISH")  
  def processMessage():
    timeout = time.time() + 60*1 - 10
    while True:  
      while not queue.empty():
        #Pause clock thread 
        message = queue.get()
        screenFlash()
        while time.time() < timeout:
          sphd.write_string("  " + message + "  >>")
          sphd.set_brightness(0.5)
          sphd.show()
          sphd.scroll(1)
          time.sleep(0.05)
        sphd.clear()
        sphd.show()
    #Resume clock thread but keep this checking for messages
    def screenClear():
      sphd.clear()
      sphd.show()
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
logging.debug("gets here")
print queue.get()
#hello = MessageListener()
#hello.__init__()
#hello.run()
#hello.listen()




