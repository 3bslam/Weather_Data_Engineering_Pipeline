import requests
import json
from datetime import datetime




governorates = [
    "Cairo", "Giza", "Alexandria", "Aswan", "Luxor", "Suez",
    "Port Said", "Ismailia", "Damietta", "Fayoum", "Beni Suef",
    "Minya", "Qena", "Sohag", "Assiut", "Marsa Matruh"
]

api_key = "7012d1d753444d94bce165541251007"
base_url = "http://api.weatherapi.com/v1/current.json"

def fetch_weather():
    all_weather_data = []

    for city in governorates:
        try:
            params = {
                "key": api_key,
                "q": city,
                "aqi": "no"
            }

            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            all_weather_data.append(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city}: {e}")

    return all_weather_data
if __name__ == "__main__":
    weather_data = fetch_weather()
    #print(weather_data)

    # for item in weather_data:
    #     print("="*40)
    #     print(f"City: {item['city']}")
    #     print(f"Temperature: {item['temperature']}°C")
    #     print(f"Condition: {item['condition']}")
    #     print(f"Humidity: {item['humidity']}%")
    #     print(f"Wind: {item['wind_kph']} kph")
    #     print(f"Local Time: {item['local_time']}")
    #     print(f"Timezone: {item['tz']}")