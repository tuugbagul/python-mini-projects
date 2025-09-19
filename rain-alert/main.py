import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
api_key = os.getenv("TWILIO_API_KEY")
twilio_phone_number= os.getenv("TWILIO_PHONE_NUMBER")
my_phone_number = os.getenv("MY_PHONE_NUMBER")

parameters = {
    "lat": 41.008240,
    "lon": 28.978359,
    "appid": api_key,
    "cnt":4,
}

will_rain = False
response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
       will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_=twilio_phone_number,
        to=my_phone_number,
    )
    print(message.status)


