from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain quantum computing in simple terms."
)

print(response.text)

print("\nToken Usage:")
print(f"Prompt tokens : {response.usage_metadata.prompt_token_count}")
print(f"Output tokens : {response.usage_metadata.candidates_token_count}")
print(f"Total tokens  : {response.usage_metadata.total_token_count}")