import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong file .env")

client = genai.Client(api_key=api_key)

print("Các model hỗ trợ generateContent:")
for m in client.models.list():
    if "generateContent" in (m.supported_actions or []):
        print(m.name)