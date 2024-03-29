from django.core.validators import RegexValidator
from twilio.rest import Client
from decouple import config

phone_regex = RegexValidator(
    regex=r'^\+998([- ])?(90|91|93|94|95|98|99|33|97|71|88|)([- ])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$',
    message='Invalid phone number'
)

# def send_phone_numer(phone, code):
#     account_sid = config('account_sid')
#     auth_token = config('auth_token')
#     client = Client(account_sid, auth_token)
#     client.messages.create(
#         body=f" Your code  {code}",
#         from_=config('from_'),
#         to=phone
#     )


def send_phone_numer(phone, code):
    print(f"Sending code {code} to phone number {phone}")




