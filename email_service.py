"""SMTP delivery for messages submitted through the portfolio contact form."""

import smtplib
import ssl
from email.message import EmailMessage


class ContactDeliveryError(Exception):
    """Raised when contact email settings are missing or SMTP delivery fails."""


def send_contact_message(name, sender_email, message, config):
    """Send a plain-text contact message through configured SMTP settings."""
    required_settings = (
        "CONTACT_RECIPIENT",
        "SMTP_HOST",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
    )
    if any(not config.get(setting) for setting in required_settings):
        raise ContactDeliveryError("Contact email settings are incomplete.")

    email = EmailMessage()
    email["Subject"] = "New portfolio contact message"
    email["From"] = config["SMTP_USERNAME"]
    email["To"] = config["CONTACT_RECIPIENT"]
    email["Reply-To"] = sender_email
    email.set_content(f"Name: {name}\nEmail: {sender_email}\n\n{message}")

    host = config["SMTP_HOST"]
    port = int(config.get("SMTP_PORT", 587))
    try:
        if port == 465:
            with smtplib.SMTP_SSL(
                host, port, timeout=10, context=ssl.create_default_context()
            ) as server:
                server.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
                server.send_message(email)
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
                server.send_message(email)
    except (OSError, smtplib.SMTPException, ValueError) as error:
        raise ContactDeliveryError("SMTP delivery failed.") from error
