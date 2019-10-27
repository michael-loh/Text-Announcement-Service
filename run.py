from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
import sys

app = Flask(__name__)

callers = []

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""

    client = Client('ACb97b4012e1468f693001a1b6c9dec35a', '57071b302d67563af02b46990d218499')
    
    mbody = request.values.get('Body', None)
    pNumber = request.values.get('From')

    mbody = mbody.lower()
    
    print(mbody)
    print(pNumber)

    resp = ''

    if mbody == 'opt in':
        
        if not pNumber in callers:
            resp = 'Your phone number has been saved \nopt in: opt into announcements \nopt out: opt out of announcements \nannouncements: <announcement>: sends announcement to group'
            callers.append(pNumber)
        else:
            resp = 'Your phone number has already been saved'
    elif mbody == 'opt out':
        
        if pNumber in callers:
            callers.remove(pNumber)
            resp = 'You have opted out'
        else:
            resp = 'Not opted in'

    elif len(mbody) >= 14 and mbody[0:13] == 'announcement:' and pNumber in callers:
        for num in callers:
            announcement = client.messages.create(to=num, from_='8184852062', body=mbody)
        resp = 'Announcment sent'
        
    else:
        resp = 'Invalid Input'
   
    try:
        message = client.messages.create(to=pNumber, from_='8184852062', body=resp)
        print(message.sid)
    except:
        print(sys.exc_info()[0])
        resp = 'starting up'        


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
