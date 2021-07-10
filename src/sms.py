import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_msg(body="some body", to=""):
    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_AUTH_KEY']
    client = Client(account_sid, auth_token)
    twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
    my_phone_number = os.environ['MY_PHONE_NUMBER']

    message = client.messages.create(
                                body=body,
                                from_=twilio_phone_number,
                                to=my_phone_number
                            )

    print(message.sid)
