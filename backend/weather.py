
import requests


def get_weather(lat, lon):

    API_KEY = "9e6614b6fce77c243c51736f4ae74640"


    url = "https://api.openweathermap.org/data/2.5/weather"


    params = {

        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"

    }



    try:

        res = requests.get(
            url,
            params=params,
            timeout=10
        )


        data = res.json()



        temp = data["main"]["temp"]

        humidity = data["main"]["humidity"]


        # real weather condition

        condition = (
            data["weather"][0]["main"]
            if "weather" in data
            else "Unknown"
        )



        description = (
            data["weather"][0]["description"]
            if "weather" in data
            else "Unknown"
        )



        rain = (
            data.get("rain", {})
            .get("1h", 0)
        )



        if rain > 0:

            rain_status = "Currently raining: YES"

        else:

            rain_status = "Currently raining: NO"





        # farming advice

        if rain > 0:

            farming = "Good for irrigation"

        elif temp > 35:

            farming = "High heat - monitor irrigation"

        else:

            farming = "Avoid unnecessary watering"





        return {


            "temp":
            temp,


            "humidity":
            humidity,


            "rain":
            rain,


            "condition":
            condition,


            "description":
            description,


            "rain_status":
            rain_status,


            "farming":
            farming

        }



    except Exception as e:


        print(
            "Weather Error:",
            e
        )


        return None
