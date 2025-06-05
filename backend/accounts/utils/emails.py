from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

from accounts.models.users import UserAccount
from accounts.utils.general import generate_token, encrypt_token


SENDER = "AAMUSTED Teaching Internship Portfolio"
PROTOCOL = config("PROTOCOL", default="http")
DOMAIN = config("DOMAIN", default="localhost:5173")


def password_reset_email(user: UserAccount, email_addr: str) -> bool:
    """
    Send password reset email to user
    """
    subject = "Password Reset Token"
    token = encrypt_token(generate_token(user))

    sender = SENDER
    receiver = [email_addr]
    html_content = render_to_string(
        "accounts/emails/password_reset_email.html",
        {
            "user": user,
            "token": token,
            "receiver": email_addr,
            "protocol": PROTOCOL,
            "domain": DOMAIN,
        },
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email.attach_alternative(html_content, "text/html")

    if email.send():
        return True
    return False


def password_reset_success_email(user: UserAccount, email_addr: str) -> bool:
    """
    Send password reset success email to user
    """
    subject = "Password Reset Successful"
    sender = SENDER
    receiver = [email_addr]
    html_content = render_to_string(
        "accounts/emails/password_reset_success_email.html",
        {"user": user, "receiver": email_addr},
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email.attach_alternative(html_content, "text/html")

    if email.send():
        return True
    return False
