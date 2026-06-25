import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

def get_ai_advice(data):

    prompt = f"""
You are Z Agro Intelligence AI.

Farm analysis:

Location:
{data.get("location")}

Crop:
{data.get("crop")}

NDVI:
{data.get("ndvi")}

Land Type:
{data.get("land_type")}

Temperature:
{data.get("temperature")} C

Humidity:
{data.get("humidity")} %

Give:

1. Crop health
2. Irrigation advice
3. Possible risks
4. Farmer action steps

Keep answer short and practical.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text