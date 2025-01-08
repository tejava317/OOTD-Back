import google.generativeai as genai
import json
from app.core.config import settings

class Gemini:
    def __init__(self, gemini_api_key: str, model_name: str="gemini-1.5-flash"):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def get_response(self, prompt: str):
        return self.model.generate_content(prompt).text

if __name__ == "__main__":
    GEMINI_API_KEY = settings.GEMINI_API_KEY
    gemini = Gemini(gemini_api_key=GEMINI_API_KEY)

    actual_temp = 20
    apparent_temp = 20
    precipitation = 0
    humidity = 0
    wind_speed = 0
    condition = "Sunny"
    temp_6am = 20
    temp_12pm = 20
    temp_6pm = 20
    temp_12am = 20

    prompt = (
        "Recommend an outfit based on the following weather information.\n"
        f"Actual temperature: {actual_temp}°C\n"
        f"Apparent temperature: {apparent_temp}°C\n"
        f"Precipitation: {precipitation}mm\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed}m/s\n"
        f"Condition: {condition}\n"
        f"Temperature at 6 am: {temp_6am}°C\n"
        f"Temperature at 12 pm: {temp_12pm}°C\n"
        f"Temperature at 6 pm: {temp_6pm}°C\n"
        f"Temperature at 12 am: {temp_12am}°C\n"
        "Recommend warmer clothing if its raining or very windy.\n"
        "Recommend a thicker outer garment and slightly lighter tops if the daily temperature range is large.\n"
        "Pick an appropriate option from the following choices to complete outfit and complete json format.\n"
        "겉옷: [두꺼운 패딩, 울 코트, 경량 패딩, 가벼운 재킷, 겉옷 없음]\n"
        "상의: [두꺼운 니트, 긴팔 티셔츠, 반팔 티셔츠]\n"
        "하의: [기모 바지, 긴 바지, 반바지]\n"
        "신발 및 양말: [부츠와 두꺼운 양말, 운동화와 얇은 양말, 샌들/슬리퍼]\n"
        "Answer in Korean while adhering to the following json format.\n"
        "겉옷: \n"
        "상의: \n"
        "하의: \n"
        "신발 및 양말: \n"
    )

    response = gemini.get_response(prompt)
    print(f"Raw response: {response}")

    response = response.replace('```json', '').replace('```', '').strip()
    parsed_response = json.loads(response)

    print(parsed_response)

    print("--------------------------------")

    print("겉옷:", parsed_response["겉옷"])
    print("상의:", parsed_response["상의"])
    print("하의:", parsed_response["하의"])
    print("신발 및 양말:", parsed_response["신발 및 양말"])
