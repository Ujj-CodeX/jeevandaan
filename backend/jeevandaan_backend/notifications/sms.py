import os
from twilio.rest import Client


from config.logger import get_logger
logger = get_logger(__name__)


def get_twilio_client():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    return Client(account_sid, auth_token)


def send_sms(phone_number, message):
    """
    Send SMS via Twilio
    """
    try:
        client = get_twilio_client()
        
        # Format phone number — add +91 for India
        if not phone_number.startswith('+'):
            phone_number = f'+91{phone_number}'

        msg = client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=phone_number
        )

        logger.info("sms_sent", extra={"phone_number": phone_number, "sid": msg.sid})
        return True

    except Exception as e:
        logger.exception("sms_failed", extra={"phone_number": phone_number})
        return False


def send_whatsapp(phone_number, message):
    try:
        client = get_twilio_client()

        if not phone_number.startswith('+'):
            phone_number = f'+91{phone_number}'

        # Get sandbox number from dashboard exactly
        sandbox_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

        if not sandbox_number:
            logger.warning("whatsapp_sandbox_number_missing", extra={
                "phone": phone_number,
            })
 

        msg = client.messages.create(
            body=message,
            from_=f'whatsapp:{sandbox_number}',  
            to=f'whatsapp:{phone_number}'
        )

        logger.info("whatsapp_sent", extra={"phone_number": phone_number, "sid": msg.sid})
        return True

    except Exception as e:
        logger.exception("whatsapp_failed", extra={"phone_number": phone_number})
        return False