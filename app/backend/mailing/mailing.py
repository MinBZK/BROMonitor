from email.message import EmailMessage
import logging
import smtplib
import os

log = logging.getLogger(__name__)

DEFAULT_SENDER = os.environ.get("APPLICATION_MAIL_ADDRESS", "bromonitor@domain.nl")
EMAIL_DOMAIN = "@domain.nl"

def send_notificatie_mail(receivers: list[str], subject: str, message: str):
    """
    Sends a notification mail individually to all receivers.
    """
    for receiver in receivers:
        sender = DEFAULT_SENDER
        if not sender or not sender.endswith(EMAIL_DOMAIN):
            log.info("Cannot send email since no or incorrect sender mail address is configured.")
            return

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(message)
        
        session = smtplib.SMTP('mail-relay')
        session.send_message(msg, sender, receiver)
    log.info(f"Succesfully sent notification mail to: {receivers}")