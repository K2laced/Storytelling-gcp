import functions_framework
import requests
import json
import os

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ Environment variable GEMINI_API_KEY is not set")

@functions_framework.http
def gemini_call(request):
    request_json = request.get_json()

    if not request_json or "prompt" not in request_json or "schema" not in request_json:
        return ("❌ Missing 'prompt' or 'schema' in JSON body.", 400, {"Access-Control-Allow-Origin": "*"})

    prompt_text = request_json["prompt"]
    schema = request_json["schema"]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}

    # Gemini prompt
    system_prompt = f"""Please respond in JSON format matching this schema (keys must not change): {json.dumps(schema)}"""

    data = {
        "contents": [
            {
                "parts": [{"text": system_prompt + "\n\nPrompt:\n" + prompt_text}]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "topP": 0.95,
            "topK": 40,
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return (content, 200, {"Access-Control-Allow-Origin": "*"})
    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, {"Access-Control-Allow-Origin": "*"})
