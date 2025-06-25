# Los Mirlos Storytelling — Project Documentation

Welcome to **Los Mirlos Storytelling**, a magical serverless app built with Google Cloud Functions and powered by Gemini (Google's LLM) — designed to craft, extend, and chat with original AI-generated stories in real time.

> Tell a story, shape the path, chat with the characters. It’s storytelling like never before.

## Team Members

* Luigi Cabrera  
* Fabián Concha  
* Alexander Gómez  
* Camila Luque  
* Sharon Valdivia  

---

## Introduction

Los Mirlos Storytelling is an interactive, **stateless** serverless application on Google Cloud Platform. Every request supplies the necessary prompt—whether to **create** a new story, **decide** how it will continue , or **chat** with a character. The Cloud Function invokes the LLM and returns the generated text immediately. 

---

## Structure
- `functions/`: Directory containing all Cloud Function source code  
  - `create_story/`: Source for the “create-story” endpoint  
  - `continue_story/`: Source for the “continue-story” endpoint  
  - `end_story/`: Source for the “end-story” endpoint  
  - `characters_chat/`: Source for the “characters-chat” endpoint  
- `static/`: Directory for static assets  
  - `figs/`: Figures and supporting scripts   
  - `script.js`: Client-side JavaScript for interactive behavior  
- `templates/`: HTML templates for the frontend  
  - `index.html`: Main single-page UI layout  
- `README.md`: Project documentation and usage instructions  
- `app.py`: Main Python application entry point defining HTTP handlers and GCS interactions  


---

## Dependencies

**Backend (Cloud Functions / `app.py`)**

* `google-cloud-aiplatform` — to call the Gemini 1.5 Flash model  
* `flask`  

**Frontend**

* Plain **HTML5** (`index.html`)  
* **JavaScript** (`script.js`) using the Fetch API

---

## Models Employed (Serverless)

* **Gemini 1.5 Flash** LLM for all story-generation and character-chat tasks  
* **Google Cloud Functions (Gen2)** to host HTTP-triggered endpoints  

---

## Functional Features

- **Story Generation**: Create a brand-new story from a short user prompt using the Gemini LLM.  
- **Story Continuation**: Append new scenes to an existing story based on user guidance, maintaining narrative context.  
- **Story Completion**: Generate a coherent, satisfying ending by selecting one of the available continuation options.  
- **Character Chat**: Role-play conversations with any character in the story, feeding persona and dialogue history to the LLM.  
- **Cloud Storage Persistence**: Save and retrieve story objects (title, characters, narrative text, continuations) as JSON files in Google Cloud Storage.  
- **RESTful API**: Expose four HTTP endpoints (`create-story`, `continue-story`, `end-story`, `characters-chat`) for easy integration.  
- **Serverless Architecture**: Leverage Google Cloud Functions Gen2 for auto-scaling, stateless execution, and pay-per-use billing.  
- **Error Handling**: Validate inputs, handle missing parameters or storage failures, and return meaningful HTTP status codes and error messages.  
- **Unique Story IDs**: Generate and return a unique identifier for each story to support retrieval and updates.  
- **Frontend Integration**: Provide a simple HTML/JS UI or third-party client via URL endpoints to interact with the service.  
- **Extensibility Hooks**: Easily add features such as user authentication, analytics tracking, or automatic illustration generation.  
- **Monitoring & Logging**: Integrate with Cloud Logging/Monitoring for tracing function invocations, performance metrics, and error alerts.  

---

## File Descriptions

### app.py
This is the main application entry point. It defines HTTP handlers for each of the four endpoints of the serverless part, parses incoming requests, calls the Gemini API, orchestrates reads and writes to Google Cloud Storage, and returns JSON responses. It also handles error cases (missing parameters, storage failures, LLM errors) and sets appropriate HTTP status codes.

### index.html
Located in the `templates` folder, this is the single-page user interface. It includes form elements for entering the initial story prompt, buttons for “Continue” and “End” actions, and a chat panel for character conversations. The page loads the CSS stylesheets from `static/css`, binds event listeners on its controls, and injects text and options into the DOM based on responses from the backend.

### scripts/
This directory under `static` contains all client-side JavaScript modules. The primary script registers event handlers on the form and buttons, sends `fetch` requests to `create-story`, `continue-story`, `end-story` and `characters-chat` endpoints, processes JSON responses, updates the HTML view (story text, continuation links, chat responses), and manages UI state (loading indicators, error messages, button disabling). It also centralizes API URL definitions and common utility functions for DOM manipulation and error handling.

---

## Available Functions (Endpoints)

### `create-story`
- **Input:** `{ "prompt": "..." }`
- **Output:** Full story, title, characters, and two continuation ideas
- **Purpose:** Generate the beginning of a brand-new story.
- **Description:** This endpoint produces a title, identifies the main characters, writes the first scene of the narrative, and returns two suggestions for how the story could continue. The function saves the resulting story object (including title, characters, text and continuations) as a JSON file in Cloud Storage and returns a unique story ID for later use.

```bash
curl -X POST https://<REGION>-<PROJECT>.cloudfunctions.net/create-story \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A brave knight ventures into the dark forest."}'
```

### `continue-story`
- **Input:** `{ "id": "story-id", "prompt": "..." }`
- **Output:** Updated story with the continuation applied
- **Purpose:** Continue an existing story using a guided idea.
- **Description:** This endpoint retrieves the existing story from Cloud Storage, re-submits the full narrative history plus the user’s new guidance to Gemini, and appends the next scene. It also regenerates two new continuation suggestions based on the updated context, saves the augmented story back to Cloud Storage, and returns the updated story text and options.

```bash
curl -X PUT https://<REGION>-<PROJECT>.cloudfunctions.net/continue-story \
  -H "Content-Type: application/json" \
  -d '{"id":"story-id-123","prompt":"The knight discovers a shimmering lake."}'
```
### `end-story`
- **Input:** `{ "id": "story-id" }`
- **Output:** Complete story with a closing scene
- **Purpose:** Use one of the possible continuations to write a satisfying ending.
- **Description:** This endpoint takes a story ID, loads the current story from Cloud Storage, selects one of the available continuation prompts, and instructs Gemini to generate a coherent, satisfying closing scene. The completed narrative overwrites the previous JSON file and the full finished text is returned in the response.

```bash
curl -X PUT https://<REGION>-<PROJECT>.cloudfunctions.net/end-story \
  -H "Content-Type: application/json" \
  -d '{"id":"story-id-123"}'
```

### `characters-chat`
- **Input:** `{ "id": "story-id", "character": "Name", "question": "..." }`
- **Output:** The character's response as if they were real
- **Purpose:** Roleplay and talk with your favorite characters.
- **Description:** This endpoint enables role-play conversations with any character from a given story. The client supplies a story ID, the character’s name, and a question. The function reconstructs the character’s persona and dialogue history, sends that context to Gemini and returns the character’s in-character reply as plain text.

```bash
curl -X POST https://<REGION>-<PROJECT>.cloudfunctions.net/characters-chat \
  -H "Content-Type: application/json" \
  -d '{"id":"story-id-123","character":"The Sorceress","question":"What is your greatest fear?"}'
```

---

## Conclusions

Los Mirlos Storytelling demonstrates how a serverless architecture on Google Cloud Platform enables the creation of scalable, cost-effective, and low-maintenance AI services. By leveraging Gemini 1.5 Flash and Cloud Functions, we achieve:

- **Automatic scaling** to handle varying loads  
- **Stateless functions** that minimize single points of failure  
- **Pay-per-use pricing** for economical operation  
- **Seamless integration** with other GCP services for future expansion  

Future enhancements could include user authentication, automatic illustration generation for each scene, interaction analytics, and a dedicated web or mobile frontend that consumes these RESTful endpoints.

---

## Demonstration

You can view a demo of the application in action here:

[Demo Video](https://drive.google.com/file/d/1vcV3sKLcJGu5XoW9_QT2STdTCDUraA-Y/view?usp=sharing)

---



