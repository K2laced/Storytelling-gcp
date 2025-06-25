import functions_framework
import uuid
import json
from google.cloud import storage
import requests
import os

BUCKET_NAME = "storys-json"  # Replace with your bucket name
GEMINI_CALL_URL = "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/gemini-call"

@functions_framework.http
def create_story(request):

    if request.method == 'OPTIONS':
        # CORS preflight
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)


    request_json = request.get_json()
    prompt = request_json.get("prompt")

    schema = {
        "title": "string",
        "story": "string",
        "characters": ["string"],
        "continuations": ["string", "string"]
    }

    gemini_payload = {
        "prompt": prompt,
        "schema": schema
    }

    response = requests.post(GEMINI_CALL_URL, json=gemini_payload)
    story_data = json.loads(response.text)

    story_id = str(uuid.uuid4())
    story_data["id"] = story_id

    # Save to Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"stories/{story_id}.json")
    blob.upload_from_string(json.dumps(story_data), content_type="application/json")

    return (json.dumps(story_data), 200, {"Access-Control-Allow-Origin": "*", 'Content-Type': 'application/json'})
