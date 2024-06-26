from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings




def detectUser(user):
  if user.role == 1:
    redirectUrl = "vendordashboard"
    return redirectUrl
  elif user.role == 2:
    redirectUrl = "custdashboard"
    return redirectUrl
  elif user.role == None and user.is_superadmin:
    redirectUrl = "/admin"
    return redirectUrl


# def send_verification_email(request, user):
#     current_site = get_current_site(request)
#     mail_subject = "Please activate your account"
#     from_email = settings.EMAIL_HOST_USER
#     # from_email = 'josephntion@gmail.com'
#     message = render_to_string("accounts/emails/account_verification_email.html", {
#         "user": user,
#         "domain": current_site.domain,
#         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#         "token": default_token_generator.make_token(user),
#     })
#     to_email = user.email

#     # Use mail context manager
#     with get_connection() as connection:
#         email = EmailMessage(
#             subject=mail_subject,
#             body=message,
#             from_email=from_email,
#             to=[to_email],
#             connection=connection,
#         )
#         email.send()


# def send_password_reset_email(request, user):
#   current_site = get_current_site(request)
#   mail_subject = "Reset your password"
#   from_email = settings.EMAIL_HOST_USER
#   # from_email = 'josephntion@gmail.com'
#   message = render_to_string("accounts/emails/reset_password_email.html", {
#       "user": user,
#       "domain": current_site.domain,
#       "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#       "token": default_token_generator.make_token(user),
#   })
#   to_email = user.email

#   # Use mail context manager
#   with get_connection() as connection:
#       email = EmailMessage(
#           subject=mail_subject,
#           body=message,
#           from_email=from_email,
#           to=[to_email],
#           connection=connection,
#       )
#       email.send()

def send_notification(mail_subject, mail_template, context):
  from_email = settings.DEFAULT_FROM_EMAIL
  message = render_to_string(mail_template, context)
  to_email = context["user"].email
  mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
  mail.send()
  return