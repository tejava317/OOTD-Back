import google.generativeai as genai

class Gemini:
    def __init__(self, gemini_api_key: str, model_name: str="gemini-1.5-flash"):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def get_response(self, prompt: str):
        return self.model.generate_content(prompt).text
