import gradio as gr
import requests

# You can use any free weather API, here we'll use Open-Meteo (no API key required)
def get_weather(city):
    try:
        # Simple way: use geocoding API to get lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if "results" not in geo_response:
            return "City not found. Try again!"

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # Weather API
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url).json()

        temp = weather_response["current_weather"]["temperature"]
        wind = weather_response["current_weather"]["windspeed"]

        return f"🌍 City: {city}\n🌡️ Temperature: {temp} °C\n💨 Wind Speed: {wind} km/h"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio interface
iface = gr.Interface(
    fn=get_weather,
    inputs=gr.Textbox(label="Enter City Name"),
    outputs=gr.Textbox(label="Weather Forecast"),
    title="🌦️ Weather Forecast App",
    description="Enter a city name to get the current weather (temperature & wind speed)."
)

if __name__ == "__main__":
    iface.launch()
