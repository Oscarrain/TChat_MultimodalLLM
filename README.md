# AI Assistant Project 2024

This project is part of the "Programming Practice" course, where we developed a comprehensive AI assistant using LocalAI and various models. The AI assistant can interact through text, generate images, understand and respond to voice commands, summarize files, and perform image classification.

## Features

1. **Interactive Chat**: The AI assistant can chat with users, remembering the context of the conversation.
2. **Streaming Responses**: Responses are provided in a streaming format for faster interaction.
3. **Web Search**: The assistant can fetch the latest information using search commands.
4. **Web Page Summarization**: The assistant can read and summarize web content.
5. **Image Generation**: Users can generate images using textual descriptions.
6. **Speech Recognition**: The assistant can convert uploaded `.wav` audio files to text.
7. **Text-to-Speech**: The assistant can convert text responses into audio replies.
8. **File Chat**: Users can upload text files, and the assistant can answer questions based on the file content.
9. **Function Calls**: The assistant can perform tasks like fetching the weather or managing a to-do list.
10. **Image Classification**: The assistant classifies uploaded images using a LeNet model trained on MNIST data.

## Installation Guide

### Prerequisites
- Docker Desktop (for model management)
- Python 3.12.4 (recommended to use Anaconda or Miniconda for environment management)
- LocalAI setup with models downloaded and placed in the `LocalAI/models` folder

### Setup Steps
1. Clone the initial repository:
   ```bash
   git clone git@git.tsinghua.edu.cn:xyz22/ai-assistant-2024.git
   ```
2. Install Docker and restart your system if using Windows.
3. Download and unzip the required models to the `LocalAI/models` directory.

### Running LocalAI
1. Start LocalAI using Docker:
   ```bash
   cd LocalAI
   docker compose up -d --pull always
   ```
2. Check if the models are running:
   ```bash
   curl http://localhost:8080/models
   ```

### Running the AI Assistant
1. Navigate to the project directory and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the AI assistant:
   ```bash
   python app.py
   ```
3. Access the assistant interface through the provided local link, usually `http://127.0.0.1:7860`.

## Usage Guide

### Basic Interaction
- Chat with the assistant through a text box.
- Use special commands like `/image description` to generate images.
- Upload files or use voice inputs to interact differently with the assistant.

### Special Commands
- `/search query`: Fetches the latest information from the web.
- `/image description`: Generates an image based on the description.
- `/audio text`: Converts text into audio.
- `/function task`: Calls specific functions like fetching the weather or adding to a to-do list.
- `/file question`: Asks questions based on uploaded text files.


## Notes
- Ensure all models are correctly configured and accessible.
- Use Anaconda or Miniconda to manage Python environments and dependencies efficiently.
