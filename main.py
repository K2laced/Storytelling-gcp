from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Variables globales simulando sesión
story_history = []
max_chapters = 10
characters = ["Anya", "Fox"]
title = "El Bosque Hablante"

# URL del endpoint LLM
LLM_ENDPOINT = "https://llm-api-901404642482.us-central1.run.app/generate"

@app.route('/')
def home():
    return render_template('index.html')

def call_llm(prompt):
    try:
        response = requests.post(
            LLM_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json={"prompt": prompt}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("output", "").strip()
        else:
            return "Error al generar contenido."
    except Exception as e:
        return f"Error de conexión con LLM: {e}"

@app.route('/generateStory', methods=['POST'])
def generate_story():
    try:
        data = request.json
        chapter = data.get('chapter', 1)
        story = data.get('story', "").strip()
        selected_option = data.get('selected_option', "").strip()
        reset = data.get('reset', False)

        if reset:
            story_history.clear()

        if chapter == 1:
            # Prompt inicial
            prompt = f"Inicia una historia infantil titulada '{title}' protagonizada por {', '.join(characters)}. El usuario propuso: '{story}'. Empieza el Capítulo 1:"
            generated_text = call_llm(prompt)

            story_part = f"\n\nCapítulo 1: {generated_text}"
            story_history.clear()
            story_history.append(story_part)
        else:
            # Continuación
            prev_story = ''.join(story_history)
            prompt = f"Continúa la historia infantil titulada '{title}' con {', '.join(characters)}. En el capítulo anterior ocurrió lo siguiente:\n{prev_story}\n\nEl usuario eligió: '{selected_option}'. Genera el Capítulo {chapter}:"
            generated_text = call_llm(prompt)

            story_part = f"\n\nCapítulo {chapter}: {generated_text}"
            story_history.append(story_part)

        # Generar opciones
        prompt_options = f"Basado en este capítulo:\n{story_part}\n\nSugiere tres posibles decisiones para continuar la historia."
        options_text = call_llm(prompt_options)
        options = [opt.strip('-•* ').strip() for opt in options_text.strip().split('\n') if opt.strip()]

        full_story = ''.join(story_history)

        response = {
            'title': title,
            'characters': characters,
            'story': full_story,
            'options': options[:3],
            'nextChapter': chapter + 1 if chapter < max_chapters else None
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
