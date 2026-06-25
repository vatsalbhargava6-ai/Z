from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from gemini_ai import get_ai_advice
from weather import get_weather
from satellite.satellite import get_satellite_analysis


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)



@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json() or {}

        lat = float(data.get("lat",0))
        lng = float(data.get("lng",0))


        # -------- REGION --------

        if lat > 23:
            region = "Northern Agro Zone"
            crop = "Soybean"

        elif lat > 22:
            region = "Central Agro Zone"
            crop = "Soybean"

        else:
            region = "Southern Agro Zone"
            crop = "Wheat"



        # -------- WEATHER --------

        try:
            weather = get_weather(lat,lng)
        except Exception as e:
            print("Weather error:",e)
            weather = {}


        temp = weather.get("temp",0)
        humidity = weather.get("humidity",0)
        rainfall = weather.get("rain",0)

        condition = weather.get("condition","Unknown")
        rain_status = weather.get("rain_status","Unknown")
        farming = weather.get("farming","No data")



        # -------- SATELLITE --------

        try:
            satellite = get_satellite_analysis(lat,lng)

        except Exception as e:
            print("Satellite error:",e)
            satellite = {}


        ndvi = satellite.get("ndvi",0)

        vegetation = satellite.get(
            "status",
            "Unknown"
        )

        land_type = satellite.get(
            "land_type",
            "Unknown"
        )

        confidence = satellite.get(
            "confidence",
            0
        )



        # -------- CROP HEALTH --------

        soil_quality = 70


        crop_health = (
            soil_quality*0.4
            +
            (100-abs(temp-28))*0.3
            +
            humidity*0.2
            +
            rainfall*0.1
        )


        crop_health += ndvi*20


        crop_health = round(
            max(0,min(100,crop_health)),
            2
        )


        if crop_health > 75:
            status="Excellent"

        elif crop_health > 50:
            status="Moderate"

        else:
            status="Poor"



        # -------- GEMINI AI --------

        try:

            ai_report = get_ai_advice({

                "location":f"{lat},{lng}",
                "crop":crop,
                "ndvi":ndvi,
                "land_type":land_type,
                "temperature":temp,
                "humidity":humidity

            })

        except Exception as e:

            print("Gemini error:",e)

            ai_report="AI unavailable"



        zones=[
            f"North - {status}",
            f"East - {status}",
            f"West - {status}",
            f"South - {status}",
            f"Center - {status}"
        ]



        return jsonify({

            "temperature":temp,
            "humidity":humidity,
            "rain":rainfall,

            "condition":condition,
            "rain_status":rain_status,
            "farming":farming,


            "region":region,
            "crop":crop,

            "crop_health_score":crop_health,
            "health_status":status,


            "ndvi":ndvi,
            "vegetation":vegetation,

            "land_type":land_type,
            "confidence":confidence,


            "ai_report":ai_report,


            "zones":zones

        })


    except Exception as e:

        print("BACKEND ERROR:",e)

        return jsonify({
            "error":str(e)
        }),500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)