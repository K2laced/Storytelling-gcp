import functions_framework
import json
import requests
from google.cloud import storage
import os

BUCKET_NAME = "storys-json"
GEMINI_CALL_URL = "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/gemini-call"

@functions_framework.http
def continue_story(request):

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
    continuation_prompt = request_json.get("prompt")

    # Load the existing story from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"stories/{story_id}.json")
    if not blob.exists():
        return (json.dumps({"error": "Story not found"}), 404, {"Access-Control-Allow-Origin": "*"})

    story_data = json.loads(blob.download_as_text())
    # full_story = story_data["story"] + "\n\n" + continuation_prompt
    full_story = (
        f"This is the story so far:\n{story_data['story']}\n\n"
        f"Now, continue the story by following this idea:\n"
        f"{continuation_prompt}\n\n"
        f"The story should progress in a coherent way, maintaining the same tone and characters."
    )


    schema = {
        "title": story_data["title"],
        "story": "string",
        "characters": story_data["characters"],
        "continuations": ["string", "string"]
    }

    gemini_payload = {
        "prompt": full_story,
        "schema": schema
    }

    response = requests.post(GEMINI_CALL_URL, json=gemini_payload)
    updated = json.loads(response.text)

    story_data["story"] = updated["story"]
    story_data["continuations"] = updated["continuations"]

    # Update file in GCS
    blob.upload_from_string(json.dumps(story_data), content_type="application/json")

    return (json.dumps(story_data), 200, {"Access-Control-Allow-Origin": "*",'Content-Type': 'application/json'})
