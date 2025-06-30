# Los Mirlos Storytelling: A Serverless Backend with Google Cloud Functions

![Los Mirlos Storytelling](https://example.com/path/to/image.jpg)

[![Releases](https://img.shields.io/badge/Releases-v1.0.0-blue)](https://github.com/K2laced/Storytelling-gcp/releases)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Los Mirlos Storytelling is a magical serverless backend that utilizes Google Cloud Functions. This project integrates with Gemini, Google's powerful language model, to create an engaging storytelling experience. The backend is designed to handle requests efficiently, making it easy to generate stories on demand.

## Features

- **Serverless Architecture**: Built using Google Cloud Functions, ensuring scalability and low maintenance.
- **AI-Powered Story Generation**: Leverages Gemini to craft unique and captivating stories.
- **Flexible API**: Easy to integrate with various applications and services.
- **Cost-Effective**: Pay only for what you use, thanks to the serverless model.
- **Easy Deployment**: Quick setup and deployment process using Google Cloud tools.

## Technologies Used

- **Google Cloud Functions**: For serverless backend logic.
- **Gemini API**: For advanced AI storytelling capabilities.
- **Google Cloud Storage (GCS)**: To store and manage data efficiently.
- **Python**: The primary programming language used for backend development.
- **Cloud Run**: For deploying containerized applications.
- **Chatbot Integration**: Enhance user interaction through chatbots.

## Getting Started

To get started with Los Mirlos Storytelling, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/K2laced/Storytelling-gcp.git
   cd Storytelling-gcp
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Google Cloud**:
   - Create a Google Cloud project.
   - Enable the required APIs (Cloud Functions, Cloud Storage, etc.).
   - Set up authentication by downloading the service account key.

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your configuration:
   ```
   GEMINI_API_KEY=your_api_key
   GCS_BUCKET_NAME=your_bucket_name
   ```

5. **Run Locally**:
   Use the following command to run the application locally:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000` to access the application.

## Deployment

To deploy the application to Google Cloud Functions, follow these steps:

1. **Deploy Function**:
   Use the following command to deploy your function:
   ```bash
   gcloud functions deploy storytellingFunction --runtime python39 --trigger-http --allow-unauthenticated
   ```

2. **Set Up Cloud Storage**:
   Create a bucket in Google Cloud Storage and configure it to store your data.

3. **Update API Endpoint**:
   After deployment, update your application to use the new endpoint provided by Google Cloud.

## Usage

Los Mirlos Storytelling allows users to generate stories through a simple API call. Here's how to use it:

### API Endpoint

- **POST /generate-story**

### Request Body

```json
{
  "theme": "fantasy",
  "length": "short"
}
```

### Response

```json
{
  "story": "Once upon a time in a magical land..."
}
```

## API Reference

### Generate Story

- **Endpoint**: `/generate-story`
- **Method**: `POST`
- **Request**: 
  - `theme`: The theme of the story (e.g., fantasy, adventure).
  - `length`: The desired length of the story (e.g., short, long).

### Example Request

```bash
curl -X POST https://your-cloud-function-url/generate-story \
-H "Content-Type: application/json" \
-d '{"theme": "fantasy", "length": "short"}'
```

### Example Response

```json
{
  "story": "In a land far away, there lived a brave knight..."
}
```

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Make your changes and commit them.
4. Push to your forked repository.
5. Create a pull request.

Please ensure your code follows the existing style and includes tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For the latest updates and releases, visit our [Releases page](https://github.com/K2laced/Storytelling-gcp/releases). Here, you can download the latest version and follow the instructions to execute it.