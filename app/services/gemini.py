import google.generativeai as genai
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
    print(gemini.get_response(
        "Who is the greatest soccer play of all time?"
    ))
