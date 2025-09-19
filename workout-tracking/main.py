import requests
from datetime import datetime
import os

APP_ID = os.environ.get("NT_APP_ID")
API_KEY = os.environ.get("NT_API_KEY")


GENDER = "Woman"
WEIGHT_KG = 59
HEIGHT_CM = 175
AGE = 20

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()


today_date = datetime.now().strftime("%Y%m%d")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        url=sheet_endpoint,
        json=sheet_inputs,
        auth=(
            "tugbagul",
            "1234567y"
          )
        )

    print(sheet_response.text)



