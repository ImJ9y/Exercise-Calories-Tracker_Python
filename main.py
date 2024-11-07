import requests
import datetime
import os

APP_ID = os.environ.get("API_ID")
APP_KEY = os.environ.get("APP_KEY")

GENDER = "MAN"
WEIGHT_KG = "80"
HEIGHT_CM = "177"
AGE = "21"

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

EXERCISE_PARMS = {
    "query": input("What exercise did you do? "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=EXERCISE_ENDPOINT, json = EXERCISE_PARMS, headers = headers)
response.raise_for_status()
data = response.json()

today = datetime.datetime.now()
DATE = today.strftime("%Y/%m/%d")
TIME = today.strftime("%H:%M:%S")

GOOGLE_SHEET_NAME = "workout"
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]

for exercise in data["exercises"]:
    sheet_inputs ={
        GOOGLE_SHEET_NAME: {
            "date": DATE,
            "time": TIME,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }


# Sheety Authentication Option 1: No Auth
"""
sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)
"""

# Sheety Authentication Option 2: Basic Auth
sheet_response = requests.post(
    sheet_endpoint,
    json=sheet_inputs,
    auth=(
        os.environ["ENV_SHEETY_USERNAME"],
        os.environ["ENV_SHEETY_PASSWORD"],
    )
)

# Sheety Authentication Option 3: Bearer Token
"""
bearer_headers = {
    "Authorization": f"Bearer {os.environ['ENV_SHEETY_TOKEN']}"
}
sheet_response = requests.post(
    sheet_endpoint,
    json=sheet_inputs,
    headers=bearer_headers
)    
"""
print(f"Sheety Response: \n {sheet_response.text}")