import functions_framework
import json
import requests
from google.cloud import storage

BUCKET_NAME = "storys-json"
GEMINI_CALL_URL = "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/gemini-call"

@functions_framework.http
def end_story(request):

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

    if not story_id:
        return ("Missing 'id'", 400, {"Access-Control-Allow-Origin": "*"})

    # Load story from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"stories/{story_id}.json")

    if not blob.exists():
        return (json.dumps({"error": "Story not found"}), 404, {"Access-Control-Allow-Origin": "*"})

    story_data = json.loads(blob.download_as_text())

    full_prompt = (
        f"{story_data['story']}\n\n"
        f"Continue and conclude the story in a satisfying way using this direction: "
        f"{story_data['continuations'][0]}"
    )

    schema = {
        "title": story_data["title"],
        "story": "string",
        "characters": story_data["characters"]
    }

    payload = {
        "prompt": full_prompt,
        "schema": schema
    }

    response = requests.post(GEMINI_CALL_URL, json=payload)
    final_data = json.loads(response.text)

    final_data["id"] = story_id

    # Overwrite story without continuations
    blob.upload_from_string(json.dumps(final_data), content_type="application/json")

    return (json.dumps(final_data), 200, {"Access-Control-Allow-Origin": "*", 'Content-Type': 'application/json'})
