from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import time
import scrollphathd as sphd

account_sid = "ACcd55cecad9957ea8780354bb06c7590d"
auth_token = "8511ba7054532277db3dc8b144693777"
#client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def hello_monkey():
 
    """Respond to incoming calls with a simple text message."""
    newMsg = 1
    fromNo = request.form['From']
    msgBdy = request.form['Body']
    print "From:", fromNo
    print "Saying:", msgBdy
    resp = MessagingResponse()
    resp.message("Message displayed on pi ! You can send a new one now !")
    screenFlash()
    sphd.write_string("  " + msgBdy + "  >>")
    sphd.set_brightness(0.5)
    timeout = time.time() + 60*1 - 10
    
    while time.time() < timeout:
      sphd.show()
      sphd.scroll(1)
      time.sleep(0.05)
    
    sphd.clear()
    sphd.show()
    print str(resp)
    return str(resp)

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
  
    
if __name__ == "__main__":
    app.run(debug=True)
