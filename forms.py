"""Validated forms used by the portfolio."""

import re

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm


_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+\Z"
)


def validate_email_address(_form, field):
    """Check basic email-address structure without an extra dependency."""
    if not _EMAIL_PATTERN.fullmatch(field.data or ""):
        raise ValidationError("Enter a valid email address.")


class ContactForm(FlaskForm):
    """Contact form with server-side validation and a bot honeypot."""

    name = StringField(
        "Name",
        validators=[DataRequired(message="Enter your name."), Length(max=80)],
        filters=[lambda value: value.strip() if value else value],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Enter your email address."),
            Length(max=254),
            validate_email_address,
        ],
        filters=[lambda value: value.strip() if value else value],
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Enter a message."),
            Length(
                min=20,
                max=3000,
                message="Message must be between 20 and 3000 characters.",
            ),
        ],
        filters=[lambda value: value.strip() if value else value],
    )
    website = StringField("Website", validators=[Length(max=200)])
