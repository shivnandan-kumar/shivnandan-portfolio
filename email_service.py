"""SMTP delivery for messages submitted through the portfolio contact form."""

import logging
import smtplib
import ssl
from email.message import EmailMessage

logger = logging.getLogger(__name__)


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
    missing_settings = [setting for setting in required_settings if not config.get(setting)]
    if missing_settings:
        logger.error(
            "Contact SMTP configuration is missing environment variable names: %s",
            ", ".join(missing_settings),
        )
        raise ContactDeliveryError("Contact email settings are incomplete.")

    email = EmailMessage()
    email["Subject"] = "New portfolio contact message"
    email["From"] = config["SMTP_USERNAME"]
    email["To"] = config["CONTACT_RECIPIENT"]
    email["Reply-To"] = sender_email
    email.set_content(f"Name: {name}\nEmail: {sender_email}\n\n{message}")

    host = config["SMTP_HOST"]
    port = int(config.get("SMTP_PORT", 587))
    stage = "smtp_connection"
    try:
        if port == 465:
            with smtplib.SMTP_SSL(
                host, port, timeout=10, context=ssl.create_default_context()
            ) as server:
                stage = "login"
                server.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
                stage = "send_message"
                server.send_message(email)
                stage = "smtp_connection"
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                stage = "ehlo"
                server.ehlo()
                stage = "starttls"
                server.starttls(context=ssl.create_default_context())
                stage = "ehlo"
                server.ehlo()
                stage = "login"
                server.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
                stage = "send_message"
                server.send_message(email)
                stage = "smtp_connection"
    except (OSError, smtplib.SMTPException, ValueError) as error:
        smtp_code = getattr(error, "smtp_code", None)
        safe_status_code = (
            str(smtp_code)
            if isinstance(smtp_code, int) and not isinstance(smtp_code, bool)
            else "unavailable"
        )
        logger.error(
            "Contact SMTP delivery failed (stage=%s, exception_type=%s, smtp_status_code=%s)",
            stage,
            type(error).__name__,
            safe_status_code,
        )
        raise ContactDeliveryError("SMTP delivery failed.") from error
