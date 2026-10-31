from google import genai
from config import settings


client = genai.Client(
    api_key=settings.api_key
)

print("\n===== AVAILABLE GEMINI MODELS =====\n")

for model in client.models.list():
    print("Model:", model.name)
    print("Display name:", model.display_name)
    print("Supported actions:", model.supported_actions)
    print("-" * 60)