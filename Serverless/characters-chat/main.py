import functions_framework
import json
import requests
from google.cloud import storage

BUCKET_NAME = "storys-json"
GEMINI_CALL_URL = "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/gemini-call"

@functions_framework.http
def characters_chat(request):

    if request.method == 'OPTIONS':
        # CORS preflight
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    request_json = request.get_json()
    story_id = request_json.get("id")
    character = request_json.get("character")
    question = request_json.get("question")

    if not story_id or not character or not question:
        return ("Missing one or more required fields: 'id', 'character', 'question'", 400, {"Access-Control-Allow-Origin": "*"})

    # Load story
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"stories/{story_id}.json")

    if not blob.exists():
        return (json.dumps({"error": "Story not found"}), 404, {"Access-Control-Allow-Origin": "*"})

    story_data = json.loads(blob.download_as_text())

    prompt = (
        f"You are a character named '{character}' from the following story:\n\n"
        f"{story_data['story']}\n\n"
        f"Now answer this user question in character:\n"
        f"User: {question}"
    )

    schema = {
        "reply": "string"
    }

    payload = {
        "prompt": prompt,
        "schema": schema
    }

    response = requests.post(GEMINI_CALL_URL, json=payload)
    reply_data = json.loads(response.text)

    return (json.dumps(reply_data), 200, {"Access-Control-Allow-Origin": "*", 'Content-Type': 'application/json'})
