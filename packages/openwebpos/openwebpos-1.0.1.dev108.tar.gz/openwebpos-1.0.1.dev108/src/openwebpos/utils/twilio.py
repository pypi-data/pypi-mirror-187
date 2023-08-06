import os

from twilio.rest import Client

from openwebpos.blueprints.pos.models import OrderMessage


def send_message(order_id, phone, message):
    """
    Send a message to a phone number.

    Args:
        order_id (int): Order id
        phone (str): Phone number to send message to.
        message (str): Message to send.

    Returns:
        None

    Example:
        >>> send_message('+15555555555', 'Hello World!')
    """
    twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
    twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(body=message, from_=twilio_phone_number,
                                     to=phone)
    om = OrderMessage(order_id=order_id, phone=phone, message=message.body,
                      sid=message.sid)
    om.save()
    print(message.sid)
