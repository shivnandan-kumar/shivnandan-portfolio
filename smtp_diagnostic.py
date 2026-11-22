"""Safely diagnose SMTP connectivity, TLS, and authentication without sending mail."""

import os
import smtplib
import ssl
import sys


def report(stage, result, error=None):
    """Print only the stage, result, exception type, and SMTP status code."""
    fields = [f"stage={stage}", f"result={result}"]

    if error is not None:
        fields.append(f"exception_type={type(error).__name__}")
        status_code = getattr(error, "smtp_code", None)
        if isinstance(status_code, int) and not isinstance(status_code, bool):
            fields.append(f"smtp_status_code={status_code}")
        else:
            fields.append("smtp_status_code=unavailable")

    print(" ".join(fields))


def validate_reply(reply, error_type):
    """Raise a sanitized SMTP exception when a reply is unsuccessful."""
    code, _ = reply
    if not 200 <= code < 300:
        raise error_type(code, b"")


def run_diagnostic():
    server = None
    try:
        try:
            host = os.environ["SMTP_HOST"]
            username = os.environ["SMTP_USERNAME"]
            password = os.environ["SMTP_PASSWORD"]
            port = int(os.environ.get("SMTP_PORT", "587"))
            if not host or not username or not password:
                raise ValueError
        except Exception as error:
            report("configuration", "failure", error)
            return False

        tls_context = ssl.create_default_context()

        if port == 465:
            # SMTP_SSL performs the implicit TLS handshake during connect().
            try:
                server = smtplib.SMTP_SSL(timeout=10, context=tls_context)
                server.connect(host, port)
                report("smtp_connection_ssl_handshake", "success")
            except Exception as error:
                report("smtp_connection_ssl_handshake", "failure", error)
                return False
        else:
            try:
                server = smtplib.SMTP(timeout=10)
                server.connect(host, port)
                report("smtp_connection", "success")
            except Exception as error:
                report("smtp_connection", "failure", error)
                return False

            try:
                validate_reply(server.ehlo(), smtplib.SMTPHeloError)
                report("first_ehlo", "success")
            except Exception as error:
                report("first_ehlo", "failure", error)
                return False

            try:
                server.starttls(context=tls_context)
                report("starttls", "success")
            except Exception as error:
                report("starttls", "failure", error)
                return False

            try:
                validate_reply(server.ehlo(), smtplib.SMTPHeloError)
                report("second_ehlo", "success")
            except Exception as error:
                report("second_ehlo", "failure", error)
                return False

        try:
            server.login(username, password)
            report("authentication", "success")
            return True
        except Exception as error:
            report("authentication", "failure", error)
            return False

    finally:
        # Close even after connection/TLS/authentication failures. Cleanup errors
        # are deliberately suppressed and never printed.
        if server is not None:
            try:
                server.quit()
            except Exception:
                try:
                    server.close()
                except Exception:
                    pass


if __name__ == "__main__":
    sys.exit(0 if run_diagnostic() else 1)
